#!/bin/bash

echo "Attempting to connect to kafka broker at ${BOOTSTRAP_SERVER}"
HOST=$( echo ${BOOTSTRAP_SERVER} | cut -d ":" -f 1 )
PORT=$( echo ${BOOTSTRAP_SERVER} | cut -d ":" -f 2 )

while nc -z "${HOST}" "${PORT}"; ret=$?; [ "${ret}" -ne 0 ]; do
  echo "${BOOTSTRAP_SERVER} is unavailable - sleeping..."
  sleep 1
done
  echo "${BOOTSTRAP_SERVER} connection established."

echo "Starting 'assigner' service"
python main.py
exit
