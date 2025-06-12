- cd C:\kafka_2.13-3.9.0
- start zookeeper
  - .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
- start kafka 
  - .\bin\windows\kafka-server-start.bat .\config\server.properties

.\bin\windows\kafka-topics.bat --describe --topic first_topic --bootstrap-server localhost:9092

.\bin\windows\kafka-topics.bat --create --topic second_topic --replication-factor 2 --partitions 3 --bootstrap-server localhost:9092


.\bin\windows\kafka-console-consumer.bat --from-beginning --topic first_topic --property print.key=true--property key.separator=":" --bootstrap-server localhost:9092


# create a new topic
.\bin\windows\kafka-topics.bat --create --topic products.prices.changelog.multi-partitions --partitions 2 --replication-factor 1 --bootstrap-server localhost:9092

# kafka  producer
.\bin\windows\kafka-console-producer.bat --topic products.prices.changelog.multi-partitions --bootstrap-server localhost:9092 --property parse.key=true --property key.separator=:


# console consumer
.\bin\windows\kafka-console-consumer.bat --from-beginning --topic products.prices.changelog.multi-partitions --property print.partition=true --property print.key=true --bootstrap-server localhost:9092

# describe topic 
.\bin\windows\kafka-topics.bat --describe --topic products.prices.changelog.multi-partitions --bootstrap-server localhost:9092 
 ^
--property print.partition=true


## develop a scenario to handle the backpressure in kafka?
## when do we use the different acks in kafka?
## try out all the consumer config in kafka?
  - isolation_level
## scenarios when should we be using the transactional processing and when not to use ?


Transactional processing in Kafka is useful when you need **exactly-once semantics** to ensure data consistency across multiple operations.
### **✅ When to Use Transactional Processing**
1. **Financial Transactions** – Ensuring that payments, transfers, or billing updates are processed **exactly once** without duplication or loss.
2. **Event Sourcing** – When maintaining a strict sequence of events in applications like audit logs or user activity tracking.
3. **Data Synchronization** – When multiple systems rely on Kafka for **consistent updates**, such as syncing databases across microservices.
4. **Batch Processing Pipelines** – When processing large datasets where **partial failures** could lead to inconsistent results.
5. **Multi-Topic Writes** – When a producer writes to multiple topics and needs **atomicity** (either all writes succeed or none).

### **❌ When NOT to Use Transactional Processing**
1. **High-Throughput Systems** – Transactions add overhead, so if speed is more important than **exactly-once guarantees**, avoid them.
2. **Stateless Processing** – If your application does not require tracking state across multiple operations, transactions may be unnecessary.
3. **Simple Logging & Metrics** – If occasional duplicates are acceptable (e.g., logging systems), **at-least-once** delivery is sufficient.
4. **Low-Latency Applications** – Transactions introduce delays due to commit operations, making them unsuitable for real-time streaming.
5. **Single-Message Processing** – If each message is independent and does not require atomicity, transactions may be overkill.



## implement a scenario of rate limiting with the producer in kafka?

## how in the CDC pipeline you would create a DLQ


##  build a kafka consumer 
  - use a restendpoint with the kafka and push data to it.

## build a kafka producer
  - a microservice architecture where we can 
  - parallel producer pushing the data

## how can we do a 
  - different consumers reading data from the same topic
  - consumer lag and monitoring
  - how can we monitor the kafka offsets
  - producer configs : test 
    - acks
    - how can i manage the throughput 
  - consumer configs

# can single rest-api do the trick of having both the consumer and the producer?