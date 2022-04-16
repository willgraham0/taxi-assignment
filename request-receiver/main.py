import datetime
import json
import os

from flask import Flask, request
from kafka import KafkaProducer

from schemas import customer_requests_taxi

topic = os.environ["TOPIC"]
client_id = os.environ["CLIENT_ID"]
broker_host = os.environ["BROKER_HOST"]
broker_port = os.environ["BROKER_PORT"]

app = Flask(__name__)


@app.route("/taxi")
def taxi():
    """Place a "Customer-Requests-Taxi" event onto the event stream."""
    customer_id = request.args["customer_id"]
    customer_name = request.args["customer_name"]
    timestamp = datetime.datetime.now().timestamp()

    event = customer_requests_taxi(customer_id, customer_name, timestamp)
    producer = KafkaProducer(
        bootstrap_servers=f"{broker_host}:{broker_port}",
        value_serializer=lambda value: json.dumps(value).encode('utf-8'),
        client_id=client_id,
    )
    producer.send(topic=topic, value=event)

    return f"Customer #{customer_id} {customer_name} requests Taxi."
