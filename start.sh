#!/bin/bash

##################
# Initialization #
##################

#determine current OS
CURRENT_OS=$(uname -s)
echo "OS detected: $CURRENT_OS"

if [ "$1" ]; then
  FMR_HOST=$1
  if [ "$2" ]; then
    FMR_PORT=$2
  else
    FMR_PORT="80"
  fi
fi
if [ -z "$FMR_PORT" ]; then 
   #If PORT parameter is not provided, use the default port:
      FMR_PORT="8080"
fi
if [ -z "$FMR_HOST" ]; then 
   #If HOST parameter is not provided, use the default hostname/address:

   if [ "$CURRENT_OS" = "Darwin" ]; then
      # Max OS X - not tested!!!
      FMR_HOST="$(ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p' | head -1)"
   elif [ "$CURRENT_OS" = "Linux" ]; then
      # Linux
      #FMR_HOST=$(hostname -I | awk '{print $1}');
      FMR_HOST="localhost"
   else
      # Windows - using Docker Desktop
      FMR_HOST="host.docker.internal"
   fi
fi
export FMR_HOST
export FMR_PORT

#########################
# Start docker services #
#########################

echo "Starting FMR services"
docker compose -p fmr -f docker-compose-fmr.yaml up -d --quiet-pull


echo "Services started:"

docker ps
echo "FMR available at: http://$FMR_HOST:$FMR_PORT"