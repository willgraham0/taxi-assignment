import ast
import datetime
import json
import logging
import os
from typing import Optional

from kafka import KafkaConsumer, KafkaProducer
from redis import Redis

from schemas import assign_customer_to_driver

logging.basicConfig(level=logging.INFO)

bootstrap_server = os.environ["BOOTSTRAP_SERVER"]
rejected_requests_topic = os.environ["REJECTED_REQUESTS_TOPIC"]
assignments_topic = os.environ["ASSIGNMENTS_TOPIC"]
sub_topics = os.environ["SUB_TOPICS"].split(",")
client_id = os.environ["CLIENT_ID"]
group_id = os.environ["GROUP_ID"]
redis_host = os.environ["REDIS_HOST"]
redis_port = os.environ["REDIS_PORT"]
redis_db = os.environ["REDIS_DB"]

store = Redis(host=redis_host, port=int(redis_port), db=int(redis_db))
producer = KafkaProducer(
    bootstrap_servers=bootstrap_server,
    value_serializer=lambda value: json.dumps(value).encode('utf-8'),
    client_id=client_id,
)
consumer = KafkaConsumer(
    *sub_topics,
    bootstrap_servers=bootstrap_server,
    group_id=group_id,
    client_id=client_id,
)


def get_available_driver() -> Optional[str]:
    """Return an available driver."""
    for driver_id in store.scan_iter():
        if store.get(driver_id) == "AVAILABLE":
            return driver_id


def assign():
    """Assign drivers to customer taxi requests.

    Subscribe to the "requests" and "status-changes" topics.
    On a "status-changes" event, set a "driver": "status" key/value pair.
    On a "requests" event, get all drivers who have a status of "available", select the first driver,
    emit "assign-commands" event and set the driver's status to "unavailable".
    (If driver does not exist, assume driver's status is "unavailable".)
    If no drivers are available emit a rejected-request event.
    """
    try:
        for event in consumer:
            event = ast.literal_eval(event.value.decode("utf-8"))
            event_type = event["event"]

            if event_type == "CUSTOMER_REQUESTS_TAXI":
                customer_id = event["customer"]["id"]
                available_driver = get_available_driver()
                if available_driver is not None:
                    timestamp = datetime.datetime.now().timestamp()
                    assignment = assign_customer_to_driver(customer_id, available_driver, timestamp)
                    producer.send(topic=assignments_topic, value=assignment)
                    logging.info(f"Customer #{customer_id} assigned to Driver #{available_driver}.")
                else:
                    logging.info(f"No drivers are currently available.")
                    producer.send(topic=rejected_requests_topic, value=event)

            elif event_type == "DRIVER_CHANGES_STATUS":
                driver_id = event["driver"]["id"]
                status = event["status"]
                store.set(driver_id, status)
            else:
                logging.info(f"Unknown event was consumed and ignored.")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    assign()
