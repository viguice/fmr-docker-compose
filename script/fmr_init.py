from tkinter import INSERT
import bcrypt
from Crypto.Cipher import AES
import uuid
import base64
import hashlib
import os
from datetime import datetime, timezone
import mysql.connector
from mysql.connector import Error


def execute_sql_script(db_config, sql_script):
    """Execute the provided SQL script on the specified database."""
    connection = None  # Ensure connection is always defined
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Split the script into individual commands
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
        for command in commands:
          cursor.execute(command)

        connection.commit()
        print("SQL script executed successfully.")

    except Error as e:
        print(f"Error executing SQL script: {e}")
    finally:
        if connection and connection.is_connected():
          cursor.close()
          connection.close()

def hash(text: str) -> str:
    """ Hashes admin password ."""
    salt = bcrypt.gensalt(rounds=10, prefix=b"2a")
    return bcrypt.hashpw(text.encode('utf-8'), salt).decode()


def get_cipher(salt, password):
    """ AES ECB cipher with PBKDF2 derivation key."""
    key = hashlib.pbkdf2_hmac(hash_name='sha256',
                              password=password.encode('utf-8'),
                              salt=salt.encode('utf-8'),
                              iterations=1000,
                              dklen=32)

    return AES.new(key, AES.MODE_ECB)


def pad(byte_array: bytearray):
    """ PKCS5 padding."""
    pad_len = 16 - len(byte_array) % 16
    return byte_array + (bytes([pad_len]) * pad_len)


def encrypt(text, salt, password):
    """ Encrypt plain text using AES ECB cipher with PBKDF2 derivation key."""
    text = pad(text.encode('UTF-8'))

    cipher = get_cipher(salt, password)
    return base64.b64encode(cipher.encrypt(text)).decode()


def get_utc_timestamp():
    """ Get current UTC timestamp in the required format."""
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


if __name__ == "__main__":
    # Get environment variables with defaults
    fmr_user = os.environ.get('FMR_USER', 'root')
    fmr_pwd = os.environ.get('FMR_PWD', 'password')
    fmr_db = os.environ.get('FMR_DB', 'fusion_registry')
    fmr_db_user = os.environ.get('FMR_DB_USER', 'fmr_user')
    fmr_db_pwd = os.environ.get('FMR_DB_PWD', 'fmr_password')

    # Generate UUIDs for encryption
    encrypt_salt = str(uuid.uuid4())
    encrypt_password = str(uuid.uuid4())

    # Generate the current timestamp
    timestamp = get_utc_timestamp()

    # Hash admin password and encrypt database password
    security_password = hash(fmr_pwd)
    database_password = encrypt(fmr_db_pwd, salt=encrypt_salt, password=encrypt_password)

    # Create the configuration output
    config = f'''#Modified on {timestamp}
#{timestamp}
database.dialect=org.hibernate.dialect.MySQL55Dialect
database.driver=com.mysql.cj.jdbc.Driver
database.password={database_password}
database.url=jdbc\\:mysql\\://mariadb\\:3306/{fmr_db}
database.useCustomString=false
database.username={fmr_db_user}
encrypt.password={encrypt_password}
encrypt.salt={encrypt_salt}
security.password={security_password}
security.username={fmr_user}
'''

    # Write to file and also print for logging
    output_path = "/app/output/fmr.properties"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(config)
    print(config)

    # Database configuration from environment variables
    db_config = {
        'host': 'mariadb',
        'database': os.environ.get('FMR_DB', 'fusion_registry'),
        'user': os.environ.get('FMR_DB_USER', 'fmr_user'),
        'password': os.environ.get('FMR_DB_PWD', 'fmr_password'),
    }

    # SQL script for database initialization
    sql_script = """
    SET NAMES utf8mb4;
    SET FOREIGN_KEY_CHECKS = 0;

    DROP TABLE IF EXISTS `registry_certificate`;
    CREATE TABLE `registry_certificate` (
      `cname` varchar(255) NOT NULL,
      `is_admin` int(11) NOT NULL,
      `display_name` varchar(255) NOT NULL,
      `email` varchar(255) NOT NULL,
      PRIMARY KEY (`cname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    DROP TABLE IF EXISTS `registry_certificate_orgs`;
    CREATE TABLE `registry_certificate_orgs` (
      `cname` varchar(255) NOT NULL,
      `urn` varchar(255) DEFAULT NULL,
      KEY `FK42kwu95vfd9xlmxwkrslfof08` (`cname`),
      CONSTRAINT `FK42kwu95vfd9xlmxwkrslfof08` FOREIGN KEY (`cname`) REFERENCES `registry_certificate` (`cname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    DROP TABLE IF EXISTS `registry_environment`;
    CREATE TABLE `registry_environment` (
      `id` varchar(255) NOT NULL,
      `name` longtext NOT NULL,
      `url` longtext NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    DROP TABLE IF EXISTS `registry_roles_mapping`;
    CREATE TABLE `registry_roles_mapping` (
      `alias` varchar(255) NOT NULL,
      `urn` longtext NOT NULL,
      PRIMARY KEY (`alias`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    DROP TABLE IF EXISTS `registry_root_security`;
    CREATE TABLE `registry_root_security` (
      `username` varchar(255) NOT NULL,
      `is_locked` int(11) NOT NULL,
      `max_login` int(11) NOT NULL,
      `pwd` varchar(255) NOT NULL,
      PRIMARY KEY (`username`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


    DROP TABLE IF EXISTS `registry_settings`;
    CREATE TABLE `registry_settings` (
      `name` varchar(50) NOT NULL,
      `value` longtext NOT NULL,
      PRIMARY KEY (`name`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    SET FOREIGN_KEY_CHECKS = 1;
    """

    # Registry settings with environment variable overrides
    registry_settings = {
        'agree.licence': 'true',
        'default.agency': os.environ.get('FMR_DEFAULT_AGENCY', 'SDMX'),
        'http.request.useragent': 'FusionRegistry/${version}',
        'installed.version': '11.0.0',
        'registry.name': os.environ.get('FMR_NAME', 'Fusion Metadata Registry'),
        'registry.url': os.environ.get('FMR_URL', 'http://localhost'),
        'security.auth.prov': 'registry',
        'registry.colour': os.environ.get('FMR_COLOUR', '#1AC6A9'),
        'registry.supportemail': os.environ.get('FMR_SUPPORTEMAIL', 'support@metadatatechnology.com'),
        'registry.supporturl': os.environ.get('FMR_SUPPORTURL', 'https://fmrwiki.sdmxcloud.org/Main_Page'),
    }

    # Insert registry_root_security into the SQL script
    insert_registry_root_security= f"INSERT INTO `registry_root_security` VALUES ('{fmr_user}', '0', '-1', '{security_password}');"
    sql_script += f"\n{insert_registry_root_security}\n"

    # Insert registry_settings into the SQL script
    insert_settings = "INSERT INTO `registry_settings` VALUES\n"
    for key, value in registry_settings.items():
        insert_settings += f"('{key}', '{value}'),\n"
    insert_settings = insert_settings.rstrip(",\n") + ";"
    sql_script += f"\n{insert_settings}\n"

    # Execute SQL script
    execute_sql_script(db_config, sql_script)
