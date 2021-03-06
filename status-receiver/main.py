import datetime
import json
import logging
import os

from flask import Flask, request
from kafka import KafkaProducer

from schemas import driver_changes_status

logging.basicConfig(level=logging.DEBUG)

topic = os.environ["TOPIC"]
client_id = os.environ["CLIENT_ID"]
bootstrap_server = os.environ["BOOTSTRAP_SERVER"]

app = Flask(__name__)
producer = KafkaProducer(
    bootstrap_servers=bootstrap_server,
    value_serializer=lambda value: json.dumps(value).encode('utf-8'),
    client_id=client_id,
)


@app.route("/status")
def taxi():
    """Place a "Driver-Changes-Status" event onto the event stream.

    The status Must be one of: AVAILABLE, UNAVAILABLE.
    """
    driver_id = request.args["driver_id"]
    timestamp = datetime.datetime.now().timestamp()
    status = request.args["status"]
    event = driver_changes_status(driver_id, status, timestamp)
    producer.send(topic=topic, value=event)
    logging.warning(f"Driver #{driver_id} changes status to {status}.")
    return "200"
