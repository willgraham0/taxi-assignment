import json
import logging
import os

from kafka import KafkaConsumer, KafkaProducer
from redis import Redis

logging.basicConfig(level=logging.DEBUG)

broker_host = os.environ["BROKER_HOST"]
broker_port = os.environ["BROKER_PORT"]
pub_topic = os.environ["PUB_TOPIC"]
sub_topics = os.environ["SUB_TOPICS"].split(",")
client_id = os.environ["CLIENT_ID"]
group_id = os.environ["GROUP_ID"]
redis_host = os.environ["REDIS_HOST"]
redis_port = os.environ["REDIS_PORT"]
redis_db = os.environ["REDIS_DB"]

store = Redis(host=redis_host, port=int(redis_port), db=int(redis_db))
producer = KafkaProducer(
    bootstrap_servers=f"{broker_host}:{broker_port}",
    value_serializer=lambda value: json.dumps(value).encode('utf-8'),
    client_id=client_id,
)
consumer = KafkaConsumer(
    *sub_topics,
    bootstrap_servers=f"{broker_host}:{broker_port}",
    group_id=group_id,
    client_id=client_id,
)


def assign():
    """Assign drivers to customer taxi requests.

    Subscribe to the "requests" and "status-changes" topics.
    On a "status-changes" event, set "driver": "status" key/value pair.
    On a "requests" event, get all driver who have a status of "available", select the first driver,
    emit "assign-commands" event and set the driver's status to "unavailable".
    (If driver does not exist, assume driver's status is "unavailable".)
    """
    pass


if __name__ == "__main__":
    assign()
