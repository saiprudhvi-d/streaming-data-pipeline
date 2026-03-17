import pytest
from src.processing.transform_events import validate_event, detect_anomaly, transform_event, compute_window_aggregation, ProcessedEvent

VALID = {"event_id":"e1","timestamp":"2024-01-15T08:00:01","transaction_id":"txn_abc","customer_id":"cust_1","amount":142.50,"status":"completed","merchant":"Amazon","category":"retail","region":"north"}

class TestValidation:
    def test_valid_passes(self): assert validate_event(VALID)[0]
    def test_missing_field(self):
        e = {k:v for k,v in VALID.items() if k!="amount"}
        assert not validate_event(e)[0]
    def test_negative_amount(self): assert not validate_event({**VALID,"amount":-50.})[0]
    def test_invalid_status(self): assert not validate_event({**VALID,"status":"unknown"})[0]
    def test_zero_valid(self): assert validate_event({**VALID,"amount":0.})[0]

class TestAnomalyDetection:
    def test_normal_not_flagged(self): assert not detect_anomaly({**VALID,"amount":100.},95.,15.)[0]
    def test_extreme_flagged(self): assert detect_anomaly({**VALID,"amount":9999.},100.,20.)[0]
    def test_zero_std_safe(self): assert not detect_anomaly({**VALID,"amount":999.},100.,0)[0]

class TestTransform:
    def test_valid(self):
        r = transform_event(VALID)
        assert r and r.amount == 142.50
    def test_invalid_none(self): assert transform_event({"event_id":"x"}) is None
    def test_anomaly_flagged(self):
        r = transform_event(VALID, running_mean=10., running_std=2.)
        assert r and r.is_anomaly

class TestWindow:
    def test_metrics(self):
        events = [
            ProcessedEvent("e1","t1","c1",100.,"completed","2024","A","r","n"),
            ProcessedEvent("e2","t2","c2",200.,"completed","2024","B","r","s"),
            ProcessedEvent("e3","t3","c3",300.,"failed","2024","C","r","e"),
        ]
        a = compute_window_aggregation(events,"start","end")
        assert a.event_count==3 and a.total_amount==600. and a.avg_amount==200.
    def test_empty(self):
        a = compute_window_aggregation([],"s","e")
        assert a.event_count==0
