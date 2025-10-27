# The fmr-docker-compose repository

This repository contains FMR docker-compose sample files to ease deployments for developments, tests, pilots and demos using docker containers.  
They can also be used as a starting point to setup production environments, but for that they still need to be complemented with scaling, archiving, security configurations, etc.

> **IMPORTANT NOTE: This demo is pre-configured for a localhost setup and is guaranteed fully functional within the local environment. Don't hesitate to open a ticket if you have any issue with the out-of-the-box setup.  
> However, any modification to this default setup and any usage outside the local environment are at your own risks and can not be supported. This disclaimer includes e.g. adding support for HTTPS, firewall proxy and access from outside the local environment.**

## Starting docker compose services

Open a new bash (Linux) or Git Bash (Windows) terminal.
Please navigate to _$fmr-docker-compose-ROOT_ folder.

Start the docker services with the following command:

```sh
$ ./start.sh
```

On **Linux** systems the execution of this script may require _elevated privilege_.
In this case please start the script with 'sudo' command as follows:

```sh
$ sudo ./start.sh
```

When the script is executed without a parameter then it starts the services to run locally on your machine:

- On Windows and Linux the following hostname is used: localhost


If you want to make your fmr installation accessible from other computers (e.g. when installation is done on a VM in the cloud) you have to provide the hostname/ip address of your host machine, e.g. when the hostname is _fmr.myorganization.org_:

```sh
$ ./start.sh fmr.myorganization.org
```

<details>
<summary>Alternative start options</summary>

1. The root credentials when **FMR_USER** and **FMR_PWD** environment variable are **NOT set** (root/password are default values)

   ```sh
   $ ./start.sh
   ```

1. Using **FMR_USER** and **FMR_PWD** environment variables

   ```sh
   $ export FMR_USER=fmr
   $ export FMR_PWD=sdmx
   $ ./start.sh
   ```

1. Using **FMR_USER** and **FMR_PWD** environment variables inline

   ```sh
   $ FMR_USER=fmr FMR_PWD=sdmx ./start.sh
   ```

1. Using external parameter file

   ```sh
   $ source .env
   $ FMR_USER=fmr FMR_PWD=sdmx ./start.sh
   ```


</details>


When all the services started properly, you should see the list of the running services on the screen started by the script.

In case you would need to see the logs produced by the containers, please see [this section](#checking-logs-of-detached-docker-containers).

## Stopping docker compose services

In a bash (Linux) or Git Bash (Windows) terminal, please navigate to _$fmr-docker-compose-ROOT_ folder.

Execute the following script to stop the docker services:

```sh
$ ./stop.sh
```

On **Linux** systems the execution of this script may require _elevated privilege_.
In this case please start the script with 'sudo' command as follows:

```sh
$ sudo ./stop.sh
```



## Basic Docker customization options

### Initialization steps

All docker images of FMR are containerized in **Linux container images**.
As a result **there is no specific requirement on the host OS** only that it should be capable to run Linux containers.

Please make sure that the configured **TCP/IP port of FMR is allowed on your firewall**.
When **using a VM in a cloud environment** (e.g. Azure, AWS, etc.) it is also important to configure the cloud network security rules to allow the inbound access of the same ports (e.g. on Azure the inbound security rules of the VM's network security group).

Please also make sure that the TCP/IP ports you are planning to use are not yet bound to other services running on the same machine.


If you are planning to access the FMR installation from other machines also, it is important to have either **a static IP address or a hostname** that is dynamically bound to the IP of your machine running FMR docker containers.
E.g. in Azure environment a public IP address associated to the VM might be configured to be either static or to have a DNS name label.

Docker engine, docker cli and docker compose must be installed on your computer in order to use run FMR docker containers. Please see the following sections on how to install them.

#### Linux

Start a terminal session and navigate to \*$fmr-docker-compose-ROOT\* folder.

##### Grant Execute permission

In Linux system scripts must have Execute permission granted in order to be able to use them from a command shell.
To grant execute permission on the helper shell scripts included in this repository please execute the following command in _$fmr-docker-compose-ROOT_ folder:

```sh
$ chmod -R a+x */*.sh -v
```

While granting the permissions, the command displays the list of script files the Execute permission has been applied on.

##### Installation of prerequisites

For using docker compose on Linux system. Docker engine need to be installed.

See how to install docker engine on docker website: https://docs.docker.com/engine/install/ubuntu/

```
  docker --version
  Docker version 20.10.x
```

#### Windows (desktop)

##### Installation of prerequisites

Install _Docker Desktop_ from the following link: https://www.docker.com/products/docker-desktop

- _WSL 2_ mode (recommended):
  From Windows 10, version 2004 or higher another option could be to use the Docker Desktop WSL 2 backend.  
  WSL offers many advantages compared to Hyper-V solution, including performance gains.  
  Installation of Docker Desktop WSL 2 backend: https://docs.docker.com/docker-for-windows/wsl/  
  If you decide to limit the memory allocated to docker in WSL 2 mode, then you should allocate at least 8GB of RAM.  
  This can be set in `%UserProfile%\.wslconfig` file (may be missing by default), e.g.:

```
[wsl2]
memory=8GB # Limits VM memory in WSL 2 to 8 GB
processors=2 # Makes the WSL 2 VM use two virtual processors
```

- _Hyper-V_ mode:
  Installation of Docker Desktop CE (Community Edition): https://docs.docker.com/docker-for-windows/install/  
  When prompted, ensure the _Enable Hyper-V Windows Features_ option is selected on the _Configuration_ page (it is the default selection in the installer), this is required for running Linux based containers on a Windows machine.  
  When choosing Hyper-V mode, we recommend to allocate at least 8 GBs of RAM to Docker (`Settings->Resources->Advanced->Memory`), and also please add the _$fmr-docker-compose-ROOT_ folder as a Shared folder (`Settings->Resources->File Sharing`).

After installation, make sure that your Docker Desktop client uses Linux containers (which is the default setup): https://docs.docker.com/docker-for-windows/#switch-between-windows-and-linux-containers

Install _Git for Windows_ from the following link: https://gitforwindows.org/

During installation when asked, please choose MinTTY terminal emulator (default selection). Having this bash shell will let you run the unix shell scripts on your Windows environemnt to help your installation.

When the installations are done, check the version of docker by executing the following script in a Git Bash terminal window:

```sh
  docker --version
```

You shall see the following on your screen (version numbers can be higher):

```
  Docker version 20.10.x
```

In order to run docker containers, the Docker Desktop client application has to be started and running in Linux containers mode.

For editing json and yml configuration files you can use _Notepad++_ (https://notepad-plus-plus.org/downloads/) with _JSON Viewer plugin_ or any other text editor of your preference.

#### Checking logs of detached docker containers

When the containers of FMR are started with docker compose in detached mode (using the _'-d'_ parameter) the logs written by the containers are not displayed on the screen.

> At the time of writing this document, _docker-compose logs_ command does not support custom compose file names.
> It can only use the default files names (docker-compose.yml and docker-compose.yaml), therefore the usage of _docker logs_ command is described in this section.
> Although, the parameters of _docker-compose logs_ are somewhat similar to _docker logs_ command.

To display a log written by a (detached) container you will need either the _container id_ or the _name_ of the container.
The container may be stopped or running.

To see the list of containers (running and exited) use the following command:

```sh
$ docker ps -a
```

This command displays the running and exited containers. The first column of the table (_CONTAINER ID_) shows the id of the container, the last column (_NAMES_) contain the name of the container.
To display the logs written by a container **you can use either the ID or the name of the container**.

E.g.: to display the logs written by the _fmr_ service _so far_, use the following command:

```sh
$ docker logs fmr
```

The command displays the logs written by _fmr_ service on the screen and returns to the shell.

Please note that _docker logs_ command displays logs written to both standard output and standard error.
It may result in unexpected behaviour when piping (e.g. when filtering the logs using _grep_) as only the standard output is redirected to the next command in the pipe.
To overcome this issue the standard error of _docker logs_ should be redirected either to standard output or /dev/null depending on whether you want to pass the logs of standard error or not:

```sh
$ docker logs fmr 2>&1 | grep 'started in'
```

```sh
$ docker logs fmr 2>/dev/null | grep 'started in'
```

In case you want to monitor real-time the logs written by a running service, use the '_-f_' or '_--follow_' parameter.

E.g. to monitor the activity of the _mariadb_ service, use the following command:

```sh
$ docker logs mariadb -f
```

The command displays the logs written by _mariadb_ so far and does not terminate but keeps displaying the upcoming log entries of the container. The command command can be terminated by pressing _Ctrl+C_.

For further reference please see the following links:

- [docker logs](https://docs.docker.com/engine/reference/commandline/logs/)

