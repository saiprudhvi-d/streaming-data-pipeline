# Streaming Data Pipeline

![Tests](https://github.com/saiprudhvi-d/streaming-data-pipeline/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-3.7-black)

## Overview
A producer/consumer streaming pipeline for near-real-time event ingestion and processing — with schema validation, anomaly detection, windowed aggregations, and full Kafka integration via Docker Compose.

## Business Problem
An operations team needs to monitor transaction activity in near real-time — detecting anomalies and computing rolling metrics. Batch pipelines running hourly are too slow. This pipeline processes events within seconds.

## Architecture
```
[Event Producer] → JSON events → [Kafka Topic: transactions]
                                          ↓
                                  [Schema Validator]
                                   valid ↓   ↓ invalid → [Dead Letter Queue]
                                  [Stream Processor]
                                  - Anomaly detection (3σ rule)
                                  - 5s tumbling window aggregations
                                          ↓
                                   [Output Sink: Parquet/JSON]
```

## Tech Stack
Python · Apache Kafka · Docker Compose · pandas · pytest · GitHub Actions

## Setup
```bash
git clone https://github.com/saiprudhvi-d/streaming-data-pipeline
pip install -r requirements.txt

# Phase 3 — Kafka (requires Docker):
docker-compose up -d
python producer/event_producer.py --mode kafka --topic transactions
```

## Future Improvements
- Spark Structured Streaming for large-scale processing
- Schema registry with Avro serialization
- Grafana + Prometheus monitoring dashboard