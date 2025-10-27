#!/bin/bash

##################
# Initialization #
##################
FMR_URL=$1
#determine current OS
CURRENT_OS=$(uname -s)
echo "OS detected: $CURRENT_OS"
if [ -z "$FMR_PORT" ]; then 
   #If PORT parameter is not provided, use the default port:
      FMR_PORT="8080"
fi
if [ -z "$FMR_URL" ]; then 
   #If HOST parameter is not provided, use the default hostname/address:

   if [ "$CURRENT_OS" = "Darwin" ]; then
      # Max OS X - not tested!!!
      FMR_URL=$(ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p' | head -1):$FMR_PORT; 
   elif [ "$CURRENT_OS" = "Linux" ]; then
      # Linux
      #FMR_URL=$(hostname -I | awk '{print $1}');
      FMR_URL="http://localhost:$FMR_PORT"
   else
      # Windows - using Docker Desktop
      FMR_URL="http://host.docker.internal:$FMR_PORT"
   fi
elif [[ "$FMR_URL" != *:* ]]; then
   FMR_URL="http://$FMR_URL:$FMR_PORT"
fi

#########################
# Start docker services #
#########################

echo "Starting FMR services"
docker compose -p fmr -f docker-compose-fmr.yaml up -d --quiet-pull


echo "Services started:"

docker ps