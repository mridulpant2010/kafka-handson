Let me explain the key aspects of delivery semantics in Kafka and how they're implemented in the code:
At-Most-Once Delivery:
Messages may be lost but are never duplicated
Implementation:
Disable auto-commit
Commit offsets before processing the message
If processing fails, the message is lost
Use case: When message loss is acceptable but duplicates are not

At-Least-Once Delivery:
Messages are never lost but may be duplicated
Implementation:
Enable auto-commit
Process message first, then commit
If processing fails, the message will be reprocessed
Use case: When message loss is not acceptable but duplicates are okay

Exactly-Once Delivery:
Messages are delivered exactly once
Implementation:
Disable auto-commit
Use message IDs to track processed messages
Implement idempotent processing
Use transactions when possible
Use case: When neither message loss nor duplicates are acceptable



- how can i use the idempotent producer?
- how to use the 
- 