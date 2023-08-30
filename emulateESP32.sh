#!/bin/bash

# Check if enough arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <BROKER_HOST> <TOPIC>"
    exit 1
fi

BROKER_HOST="$1"
TOPIC="$2"

while IFS= read -r line; do
  mosquitto_pub -h "$BROKER_HOST" -t "$TOPIC" -m "$line"
  sleep 0.001
done < heart.csv
