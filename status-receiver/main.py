import datetime
import json
import os

from flask import Flask, request
from kafka import KafkaProducer

from schemas import driver_changes_status

topic = os.environ["TOPIC"]
client_id = os.environ["CLIENT_ID"]
broker_host = os.environ["BROKER_HOST"]
broker_port = os.environ["BROKER_PORT"]

app = Flask(__name__)


@app.route("/status")
def taxi():
    """Place a "Driver-Changes-Status" event onto the event stream."""
    driver_id = request.args["customer_id"]
    driver_name = request.args["customer_name"]
    timestamp = datetime.datetime.now().timestamp()

    # Must be one of: ONLINE, OFFLINE, AVAILABLE, UNAVAILABLE
    status = request.args["status"]

    event = driver_changes_status(driver_id, driver_name, status, timestamp)
    producer = KafkaProducer(
        bootstrap_servers=f"{broker_host}:{broker_port}",
        value_serializer=lambda value: json.dumps(value).encode('utf-8'),
        client_id=client_id,
    )
    producer.send(topic=topic, value=event)

    return f"Driver #{driver_id} {driver_name} changes status to {status}."
