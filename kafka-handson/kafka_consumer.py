from kafka import KafkaConsumer
import json
from typing import Dict, Any
from enum import Enum


class DeliverySemantics(Enum):
    AT_MOST_ONCE = "at_most_once"
    AT_LEAST_ONCE = "at_least_once"
    EXACTLY_ONCE = "exactly_once"


class KafkaMessageConsumer:
    def __init__(
        self,
        #topic: str,
        bootstrap_servers: str,
        group_id: str,
        delivery_semantics: DeliverySemantics = DeliverySemantics.AT_LEAST_ONCE
    ):
        #self.topic = topic
        self.delivery_semantics = delivery_semantics
        
        # Configure consumer based on delivery semantics
        consumer_config = {
            "bootstrap_servers": bootstrap_servers,
            "auto_offset_reset": "earliest", #latest
            "group_id": group_id,
            "value_deserializer": lambda x: json.loads(x.decode('utf-8'))
        }

        if delivery_semantics == DeliverySemantics.AT_MOST_ONCE:
            # Disable auto commit and commit before processing
            consumer_config.update({
                "enable_auto_commit": False
            })
        elif delivery_semantics == DeliverySemantics.AT_LEAST_ONCE:
            # Enable auto commit (default behavior)
            consumer_config.update({
                "enable_auto_commit": True, # where are these commits stored?
                "auto_commit_interval_ms": 5000  # Commit every 5 seconds
            })
        elif delivery_semantics == DeliverySemantics.EXACTLY_ONCE:
            # For exactly-once, we need to:
            # 1. Disable auto commit
            # 2. Use transactions
            # 3. Implement idempotent processing
            consumer_config.update({
                "enable_auto_commit": False,
                "isolation_level": "read_committed"  # Only read committed messages
            })

        self.consumer = KafkaConsumer("first_topic",**consumer_config)
        print(f"Consumer initialized for {delivery_semantics.value} semantics")

    def process_message(self, message: Dict[str, Any]) -> None:
        """
        Process a single message from Kafka.
        Override this method in your implementation.
        """
        print(f"Processing message: {message}")

    def start_consuming(self,topic) -> None:
        """
        Start consuming messages from Kafka with the configured delivery semantics.
        """
        res=[]
        try:
            print(f"Starting to consume messages from topic: {topic}")
            # TODO: how do we handle the multiple topic names.
            #self.consumer.subscribe(list(topic)) # will this step overwrite what topic i am reading previously.
            for message in self.consumer:
                try:
                    if self.delivery_semantics == DeliverySemantics.AT_MOST_ONCE:
                        # Commit before processing to ensure at-most-once
                        self.consumer.commit()
                        res.append(message.value)
                        #self.process_message(message.value)
                    elif self.delivery_semantics == DeliverySemantics.AT_LEAST_ONCE:
                        # Process first, then commit (auto-commit will handle this)
                        #self.process_message(message.value)
                        res.append(message.value)
                    elif self.delivery_semantics == DeliverySemantics.EXACTLY_ONCE:
                        # For exactly-once, we need to:
                        # 1. Check if message was already processed (using message ID)
                        # 2. Process the message
                        # 3. Store the message ID as processed
                        # 4. Commit the offset
                        message_id = message.headers.get('message_id', [b''])[0].decode()
                        if not self._is_message_processed(message_id):
                            
                            #self.process_message(message.value)
                            self._mark_message_processed(message_id)
                            self.consumer.commit()
                except Exception as e:
                    print(f"Error processing message: {e}")
                    if self.delivery_semantics == DeliverySemantics.AT_LEAST_ONCE:
                        # For at-least-once, we don't commit on error
                        # This ensures the message will be reprocessed
                        continue
            return res
        except KeyboardInterrupt:
            print("Stopping consumer...")
        finally:
            self.consumer.close()
            print("Consumer closed")


# if __name__ == "__main__":
#     # Example usage with different delivery semantics
#     consumer = KafkaMessageConsumer(
#         topic="your_topic",
#         bootstrap_servers="localhost:9092",
#         group_id="your_consumer_group",
#         delivery_semantics=DeliverySemantics.AT_LEAST_ONCE
#     )
#     consumer.start_consuming()
    
# thinks to look for:
#   auto_offset_reset?
#   enable_auto_commit


## TODO: implement the way to read the kafka topic as consumer and the other way with the message streaming.
## TODO: what metrics do you see for the kafka lag performance.
## TODO: in kafka we might face the challenge and failure might come so how we perform the automatic retries and the idempotent mode.
    ## the failure comes at the producer side  so how we will
    ## the failure comes at the consumer side so how we will handle it.

# how can you make the producer idempotent in kafka? how can you make the consumer idempotent in kafka?
# difference between ISR and the replicated partitions.
# how can you enable transactions in kafka?