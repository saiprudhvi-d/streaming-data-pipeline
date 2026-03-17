import json, time, uuid, random
from datetime import datetime
from src.utils.logger import get_logger
logger = get_logger(__name__)

MERCHANTS = ["Amazon","Walmart","Target","Starbucks","Netflix","Uber"]
STATUSES = ["completed","completed","completed","pending","failed"]
CATEGORIES = ["retail","food","entertainment","transport","subscription"]

def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "transaction_id": "txn_" + uuid.uuid4().hex[:8],
        "customer_id": "cust_" + str(random.randint(1000,9999)),
        "merchant": random.choice(MERCHANTS),
        "amount": round(random.lognormal(3.5, 1.2), 2),
        "currency": "USD",
        "status": random.choice(STATUSES),
        "category": random.choice(CATEGORIES),
        "region": random.choice(["north","south","east","west"])
    }

def publish_simulated(n=100, delay=0.05, queue=None):
    events = []
    for _ in range(n):
        e = generate_event(); events.append(e)
        if queue is not None: queue.append(e)
        logger.info("Event: " + e["transaction_id"] + " | $" + str(e["amount"]) + " | " + e["status"])
        time.sleep(delay)
    logger.info("Done: " + str(len(events)) + " events published")
    return events

def publish_kafka(topic, n=100, bootstrap="localhost:9092"):
    try:
        from kafka import KafkaProducer
    except ImportError:
        logger.error("kafka-python not installed"); return
    prod = KafkaProducer(
        bootstrap_servers=bootstrap,
        value_serializer=lambda v: json.dumps(v).encode(),
        acks="all", retries=3
    )
    for _ in range(n):
        e = generate_event()
        prod.send(topic, value=e, key=e["customer_id"].encode()).get(timeout=10)
    prod.flush(); prod.close()
