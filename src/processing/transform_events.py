import re
from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

REQUIRED = {"event_id","timestamp","transaction_id","customer_id","amount","status"}
VALID_STATUSES = {"completed","pending","failed"}

@dataclass
class ProcessedEvent:
    event_id: str
    transaction_id: str
    customer_id: str
    amount: float
    status: str
    timestamp: str
    merchant: str
    category: str
    region: str
    is_anomaly: bool = False
    anomaly_reason: str = ""

@dataclass
class WindowAggregation:
    window_start: str
    window_end: str
    event_count: int
    total_amount: float
    avg_amount: float
    anomaly_count: int
    status_breakdown: Dict[str,int] = field(default_factory=dict)

def validate_event(event):
    missing = REQUIRED - set(event.keys())
    if missing: return False, f"Missing: {missing}"
    if not isinstance(event.get("amount"),(int,float)) or event["amount"] < 0:
        return False, f"Invalid amount: {event.get('amount')}"
    if event.get("status") not in VALID_STATUSES:
        return False, f"Invalid status: {event.get('status')}"
    return True, ""

def detect_anomaly(event, running_mean, running_std):
    if running_std == 0: return False, ""
    z = abs(event["amount"] - running_mean) / running_std
    if z > 3: return True, f"Amount is {z:.1f} sigma from mean"
    return False, ""

def transform_event(raw, running_mean=0, running_std=0):
    valid, err = validate_event(raw)
    if not valid: return None
    is_anom, reason = detect_anomaly(raw, running_mean, running_std)
    return ProcessedEvent(
        event_id=raw["event_id"], transaction_id=raw["transaction_id"],
        customer_id=raw["customer_id"], amount=float(raw["amount"]),
        status=raw["status"], timestamp=raw.get("timestamp", datetime.utcnow().isoformat()),
        merchant=raw.get("merchant","unknown"), category=raw.get("category","unknown"),
        region=raw.get("region","unknown"), is_anomaly=is_anom, anomaly_reason=reason
    )

def compute_window_aggregation(events, window_start, window_end):
    if not events: return WindowAggregation(window_start,window_end,0,0,0,0)
    amounts = [e.amount for e in events]
    sc = {}
    for e in events: sc[e.status] = sc.get(e.status,0) + 1
    return WindowAggregation(
        window_start=window_start, window_end=window_end,
        event_count=len(events), total_amount=round(sum(amounts),2),
        avg_amount=round(sum(amounts)/len(amounts),2),
        anomaly_count=sum(1 for e in events if e.is_anomaly),
        status_breakdown=sc
    )
