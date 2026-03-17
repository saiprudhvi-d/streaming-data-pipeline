# Stream Design

## Flow
```
Producer -> JSON events -> Kafka Topic
                               |
                        Schema Validator
                    valid |        | invalid
                          v        v
                   Processor    Dead Letter Queue
                   - Transform
                   - Anomaly (3sigma)
                   - 5s windows
                          |
                     Output Sink
```

## Event Schema
Required: event_id, timestamp, transaction_id, customer_id, amount, status

## Windowing
5-second tumbling windows with count, total, avg, anomaly_count, status_breakdown.
