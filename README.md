# Taxi Assignment

## Introduction

## Architecture

## Usage

## Comments

1. The importance of Event Schemas.

Each microservice is totally unaware of the others but a contract does
exist between them and that is the structure of the events that they produce and 
consume. In this example the event structures are repeatedly defined in each of the 
microservices in which they are relevant. This is not ideal since if the schema of 
an event of a producing service changes then the schema definition of the consuming
service(s) need to change too. The use of Data Serialization Systems or "schema stores"
should be used that each microservice can have access to.

2. Sharding
