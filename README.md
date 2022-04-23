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

## Comments

1. The Importance of Event Schemas.

Each microservice is totally unaware of any other microservices that may exist but a 
contract of sorts does exist between them which is held in the structure of the events that 
they produce and consume. In this example the event structures are repeatedly defined in each 
of the microservices in which they are relevant as simple json. This is not ideal since if the schema of 
an event of a producing service changes then the schema definition of the consuming
service(s) need to change too. The use of a Data Serialization System or "Schema Registry"
can be used that each microservice can retrieve during the start-up phase of the application 
and subsequently use.

2. Multiple brokers/Sharding/Partitioning.

3. Capturing Failures as Events (in-band).

Internal application exceptions (known or unknown such as invalid schema validation or bugs) 
can be captured as events in themselves and placed in dedicated failure topics.

4. Restarting the applications.

Effect on offset...

[architecture]: docs/taxi-assignment.png "architecture"
