from kafka import KafkaProducer
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime


class RateLimitedKafkaProducer:
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        messages_per_second: int = 10,
        batch_size: int = 16384,
        linger_ms: int = 0
    ):
        """
        Initialize a rate-limited Kafka producer.
        
        Args:
            bootstrap_servers: Kafka broker address
            topic: Topic to produce messages to
            messages_per_second: Maximum number of messages to send per second
            batch_size: Maximum size of a batch in bytes
            linger_ms: Time to wait for more messages before sending a batch
        """
        self.topic = topic
        self.messages_per_second = messages_per_second
        self.last_send_time = 0
        self.message_count = 0
        
        # Configure producer
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            batch_size=batch_size,
            linger_ms=linger_ms,
            acks='all',  # Wait for all replicas to acknowledge
            retries=3    # Retry failed sends
        )
        print(f"Producer initialized for topic: {topic}")

    def _wait_for_rate_limit(self) -> None:
        """
        Implement rate limiting by waiting if necessary.
        """
        current_time = time.time()
        elapsed = current_time - self.last_send_time
        
        if self.message_count >= self.messages_per_second:
            # If we've sent our quota, wait until the next second
            if elapsed < 1.0:
                time.sleep(1.0 - elapsed)
            self.message_count = 0
            self.last_send_time = time.time()
        elif elapsed >= 1.0:
            # Reset counter if a second has passed
            self.message_count = 0
            self.last_send_time = current_time

    def send_message(
        self,
        message: Dict[str, Any],
        key: Optional[str] = None,
        partition: Optional[int] = None
    ) -> None:
        """
        Send a message to Kafka with rate limiting.
        
        Args:
            message: The message to send
            key: Optional key for the message
            partition: Optional partition to send to
        """
        self._wait_for_rate_limit()
        
        # Add timestamp to message
        message['timestamp'] = datetime.now().isoformat()
        
        # Send the message
        future = self.producer.send(
            self.topic,
            value=message,
            key=key.encode('utf-8') if key else None,
            partition=partition
        )
        
        # Wait for the message to be delivered
        try:
            record_metadata = future.get(timeout=10)
            self.message_count += 1
            print(
                f"Message sent to topic: {record_metadata.topic}, "
                f"partition: {record_metadata.partition}, "
                f"offset: {record_metadata.offset}"
            )
        except Exception as e:
            print(f"Error sending message: {e}")

    def close(self) -> None:
        """
        Close the producer and flush any remaining messages.
        """
        self.producer.flush()
        self.producer.close()
        print("Producer closed")




