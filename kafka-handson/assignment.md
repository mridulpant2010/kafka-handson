Here are several **medium** and **hard**-level exercises you can implement in Kafka using Python. These exercises will help you deepen your understanding of Kafka concepts, Python client libraries, and advanced Kafka features.

## Medium-Level Exercises

**1. Multi-Partition Producer and Consumer**
- Create a Kafka producer that sends messages with keys to ensure they are distributed across multiple partitions of a topic.
- Implement a consumer group with multiple consumers to read from all partitions and print which partition each message was consumed from[2][3][7].

**2. File Streaming Pipeline**
- Write a producer that reads a large file (e.g., CSV or JSON lines) and streams each line as a message to a Kafka topic.
- The consumer should reconstruct the file by consuming messages and writing them to a new file, ensuring order and completeness.

**3. Image Processing Workflow**
- Build a system where the producer watches a folder for new images and sends image metadata (or the image itself, base64-encoded) to a Kafka topic.
- The consumer processes each image (e.g., resizes or applies filters) and saves the result to another folder, logging the processing status[3].

**4. Custom Serialization/Deserialization**
- Implement custom serializers and deserializers (e.g., using Avro or JSON) for complex Python objects sent through Kafka.
- Demonstrate schema evolution by changing the object structure and updating both producer and consumer accordingly[2][4].

## Hard-Level Exercises

**1. Transactional Producer-Consumer (Exactly-Once Semantics)**
- Implement a producer that uses Kafka transactions to atomically write related events to multiple topics (e.g., order and inventory events).
- The consumer should read from both topics with `isolation_level='read_committed'` to ensure it only processes committed transactions[1][5].

**2. Idempotent Producer with Failure Handling**
- Configure a Kafka producer for idempotence to prevent duplicate messages during retries.
- Simulate network failures or broker downtime and demonstrate that no duplicates are produced when the producer recovers[5].


**5. Chained Microservices with Kafka**
- Implement a pipeline of at least three microservices, each as a separate Python process:
  - Service A: Produces raw data to Topic 1.
  - Service B: Consumes from Topic 1, processes the data, and produces to Topic 2.
  - Service C: Consumes from Topic 2 and performs final aggregation or storage.
- Ensure each service handles failures gracefully and supports at-least-once or exactly-once delivery semantics.

## Example: Transactional Producer (Hard Level)

```python
from confluent_kafka import Producer
import json

config = {
    'bootstrap.servers': 'localhost:9092',
    'transactional.id': 'order_inventory_txn'
}

producer = Producer(config)
producer.init_transactions()

order_events = [{'order_id': '101', 'product_id': 'xyz123', 'quantity': 3}]
inventory_events = [{'product_id': 'xyz123', 'quantity': -3}]

producer.begin_transaction()
try:
    for event in order_events:
        producer.produce('orders', key=event['order_id'], value=json.dumps(event))
    for event in inventory_events:
        producer.produce('inventory', key=event['product_id'], value=json.dumps(event))
    producer.commit_transaction()
except Exception as e:
    producer.abort_transaction()
    print(f"Transaction aborted: {e}")
```
This ensures that either both the order and inventory events are published together, or neither is, demonstrating atomicity[1][5].

---

These exercises will give you hands-on experience with both standard and advanced Kafka features in Python, including transactions, idempotence, exactly-once semantics, custom serialization, and stream processing frameworks like Faust[1][2][4][5].

Citations:
[1] https://github.com/confluentinc/learn-apache-kafka-for-python-developers-exercises/blob/master/solutions/kafka-python/tx_producer.py
[2] https://github.com/dpkp/kafka-python
[3] https://blog.devgenius.io/kafka-with-python-4eb017b41e83
[4] https://docs.confluent.io/kafka-clients/python/current/overview.html
[5] https://gpttutorpro.com/how-to-use-kafka-advanced-features-with-python-to-enhance-your-capabilities/
[6] https://www.youtube.com/watch?v=D2NYvGlbK0M
[7] https://dev.to/hesbon/apache-kafka-with-python-laa
[8] https://developer.confluent.io/get-started/python/
[9] https://github.com/confluentinc/learn-apache-kafka-for-python-developers-exercises/blob/master/solutions/kafka-python/consumer.py
[10] https://www.youtube.com/watch?v=5sqegy_EPa0
[11] https://github.com/pmoskovi/kafka-learning-resources
[12] https://blog.soname.solutions/apache-kafka-micro-batch-consumer-in-python-779d930b53d6
[13] https://developers.sap.com/tutorials/local-apache-kafka-python..html
[14] https://aiven.io/developer/teach-yourself-apache-kafka-and-python-with-a-jupyter-notebook
[15] https://leftasexercise.com/2020/06/12/learning-kafka-with-python-consuming-data/
[16] https://www.kai-waehner.de/blog/2023/05/28/quix-streams-stream-processing-with-kafka-and-python/
[17] https://pynative.com/python-exercises-with-solutions/
[18] https://www.youtube.com/watch?v=0giSfPI0UnM
[19] https://interviewkickstart.com/blogs/articles/advanced-python-coding-challenges

---
Answer from Perplexity: pplx.ai/share