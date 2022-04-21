#!/bin/bash

echo "Attempting to connect to kafka broker at ${BROKER_HOST}:${BROKER_PORT}"
while nc -z "${BROKER_HOST}" "${BROKER_PORT}"; ret=$?; [ "${ret}" -ne 0 ]; do
  echo "kafka broker is unavailable - sleeping..."
  sleep 1
done
  echo "kafka broker connection established."

echo "Starting 'request-receiver' service"
flask run --host=0.0.0.0
exit
