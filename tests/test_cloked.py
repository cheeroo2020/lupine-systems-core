"""Tests for Cloked-lite: evidence chain integrity."""
from src.cloked_lite.logger import create_evidence_log, append_evidence, verify_chain


def test_chain_integrity():
    log = create_evidence_log("req-1")
    log = append_evidence(log, "request_created", {"amount": 500000})
    log = append_evidence(log, "routes_generated", {"count": 3})
    log = append_evidence(log, "route_scored", {"winner": "Balanced"})
    assert verify_chain(log) is True


def test_tampered_chain_fails():
    log = create_evidence_log("req-1")
    log = append_evidence(log, "event_a", {"data": "a"})
    log = append_evidence(log, "event_b", {"data": "b"})
    # Tamper with the chain
    log.entries[0].data_hash = "tampered_hash"
    assert verify_chain(log) is False


def test_genesis_link():
    log = create_evidence_log("req-1")
    log = append_evidence(log, "first", {"x": 1})
    assert log.entries[0].previous_hash == "genesis"
