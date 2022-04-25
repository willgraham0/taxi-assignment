# Taxi Assignment

## Introduction

We want to create an event-driven Taxi Assignment application where customers 
request a taxi and are assigned to available taxi drivers making use of Apache Kafka.

## Architecture

The architecture is laid out below:

![alt text][architecture]

## Usage

To spin up the services enter the following command:

```bash
docker-compose up
```

Driver #1 signals that they are available:

```bash
http "localhost:8081/status?driver_id=1&status=AVAILABLE"
```

Customer #2 requests a taxi:

```bash
http "localhost:8080/taxi?customer_id=1"
```

Inspect the topics using `kafkacat`:

```bash
kafkacat -C -b localhost:9093 -t assign-commands
```

## Comments

1. The Importance of Event Schemas.

By using a unified log each microservice is totally decoupled from the others. However, a 
contract does exist between them which is written in the structure of the events that 
they produce and consume. If a producer were to modify the structure of an event
all the consumers of this event may need to be refactored to handle this modification. 
Additionally, any new consumers that traverse the topic crossing the point of the restructuring
would need to be aware of it.

The use of a Schema Registry can be used to mitigate this problem. A producer registers the schema with the
Registry and receives a schema ID. This is then passed along with the event data onto the topic.
Consumers of the topic now have the event data and the schema ID. The schema is retrieved from the 
Registry using this ID and the event data is then deserialized using it. By registering the schema in the 
Registry, the structure is documented and publicly available for other consumers that may come along.
However, the issue of breaking changes remains unsolved.

2. Multiple brokers/Sharding/Partitioning.

The structure of the Kafka cluster can be inspected using:

```bash
kafkacat -C -b localhost:9093 -L
```

3. Capturing Failures as Events (in-band).

Internal application exceptions (known or unknown such as invalid schema validation or bugs) 
can be captured as events in themselves and placed in dedicated failure topics.

4. Restarting the applications.

Consumers that have been restarted consume events from where they left off. This is because the offset
on each partition for a given consumer group is stored on the broker containing that partition. 

[architecture]: docs/taxi-assignment.png "architecture"
