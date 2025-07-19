## 🧪 **1. Idempotent Producer with Retry & Backoff**
'''
Write a producer that:

* Ensures exactly-once semantics (idempotent producer enabled)
* Retries with exponential backoff on transient errors
* Logs permanent errors to a DLQ topic

What it tests: producer config tuning, error handling, DLQ pattern

'''

from kafka import KafkaProducer
from datetime import datetime
producer = KafkaProducer(
    bootstrap_servers = bootstrap_servers,
    acks = 'all',
    retries = 3,
    enable_idempotence=True,
    batch_size= 65536  , #64KB
    linger_ms= 20,
    buffer_memory= 268435456  # 256 MB
)

message={}
message['timestamp'] = datetime.now().isoformat() #?: how timestamp is utilised by the broker.


#we have duplicate writes due to the retries.
try:
    producer.send(
        topic=topic,
        value = message,
        key = key.encode("utf-8") if key else none,
        #partition = partition
    )
except Exception as e:
    print(e)

producer.flush()
producer.close()

if __name__ == "__main__":
    bootstrap_servers = "localhost:9092"
    topic="first_topic"

# how do i handle the scenario when buffer exhausts (backpressure)