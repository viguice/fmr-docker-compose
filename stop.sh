#!/bin/sh 

docker compose -p fmr down
echo "Do you want to remove all FMR data? (y/n)"
read REMOVE_DATA
if [ "$REMOVE_DATA" = "y" ] || [ "$REMOVE_DATA" = "Y" ]; then
   echo "Removing all FMR data..."
   docker volume rm fmr_mariadb-data fmr_fmr-properties
   echo "All FMR data have been removed."
else
   echo "FMR data have NOT been removed."
fi
echo "FMR services stopped."