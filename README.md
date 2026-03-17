# Streaming Data Pipeline

![Tests](https://github.com/saiprudhvi-d/streaming-data-pipeline/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)

Near-real-time event streaming pipeline with schema validation, anomaly detection, and Kafka integration.

## Stack
Python · Apache Kafka · Docker Compose · pandas

## Features
- Producer/consumer architecture
- Schema validation + dead letter queue
- Anomaly detection (3σ rule)
- 5-second tumbling window aggregations
- Full Kafka via Docker Compose (Phase 3)

## Setup
```bash
git clone https://github.com/saiprudhvi-d/streaming-data-pipeline
pip install -r requirements.txt
# Phase 3 Kafka:
docker-compose up -d
```

## CI/CD
Tests run automatically on every push via GitHub Actions.