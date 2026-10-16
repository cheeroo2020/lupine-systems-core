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


def test_uncertain_then_reconciled_chain_verifies():
    log = create_evidence_log("req-1")
    log = append_evidence(log, "instruction_issued", {"id": "cmd-1", "target": 50.0})
    log = append_evidence(log, "outcome_assessed",
                          {"outcome": "uncertain", "reason": "no receipt; no reading available"})
    log = append_evidence(log, "reconciliation_attempted",
                          {"outcome": "completed", "reading": 50.4})
    assert verify_chain(log) is True


def test_rewriting_an_uncertain_verdict_breaks_the_chain():
    log = create_evidence_log("req-1")
    log = append_evidence(log, "outcome_assessed", {"outcome": "uncertain"})
    log = append_evidence(log, "reconciliation_attempted", {"outcome": "failed"})
    log.entries[0].payload["outcome"] = "completed"   # pretend it worked
    assert verify_chain(log) is False
