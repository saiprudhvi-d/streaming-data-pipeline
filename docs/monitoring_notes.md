# Monitoring Notes

## Key Metrics
- Consumer lag vs producer
- Error rate: % events failing validation
- Anomaly rate: % flagged per window

## Dead Letter Queue
Invalid events written to data/dead_letter/ with error reason attached.

## Retry Strategy
- Transient errors: retry 3x with exponential backoff
- Schema errors: DLQ immediately, no retry

## Alert Triggers
- Lag > 1000 messages
- Error rate > 5% in 1-minute window
- Zero events for > 30 seconds
