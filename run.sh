#!/bin/bash
set -euo pipefail
echo "Starting containers..."
docker-compose up -d
echo "Containers started successfully."
echo "Waiting for automation to complete..."
exit_code=`docker wait classscraper-app-1`
if [[ "$exit_code" == 0 ]]; then
  echo "Automation executed successfully."
  echo "Copying output to your local machine..."
  docker cp classscraper-app-1:/app/output.txt .
  echo "Output copied to output.txt file."
else
  echo "Automation failed."
  echo "Copying logs to your local machine..."
  docker cp classscraper-app-1:/app/logs.txt .
  echo "Logs copied to logs.txt file."
  echo "Check logs to see why automation failed."
fi
echo "Stopping selenium container..."
echo "Stopped container:"
docker stop classscraper-selenium-1
echo "Removing containers..."
echo "Removed containers:"
docker rm classscraper-selenium-1
docker rm classscraper-app-1
echo "Removing images..."
docker image rm classscraper-app
docker image rm seleniarm/standalone-chromium:114.0
echo "Bye!"