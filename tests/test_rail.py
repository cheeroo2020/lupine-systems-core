"""Tests for Rail-lite: state machine execution."""
from datetime import datetime, timedelta, timezone

import pytest
from src.rail_lite.executor import (
    create_execution, advance_state, simulate_full_execution,
    record_outcome, reconcile, safe_to_reissue,
)
from src.rail_lite.outcome import assess
from src.models.schemas import ExecutionStatus, Instruction, Observation, Receipt


def test_full_execution_completes():
    state = simulate_full_execution("req-1", "route-1")
    assert state.status == ExecutionStatus.completed
    assert len(state.state_history) == 5  # init + 4 transitions


def test_invalid_transition_raises():
    state = create_execution("req-1", "route-1")
    with pytest.raises(ValueError):
        advance_state(state, ExecutionStatus.completed)  # can't skip


def test_state_history_tracks_all():
    state = simulate_full_execution("req-1", "route-1")
    statuses = [h["to"] for h in state.state_history]
    assert statuses == [
        ExecutionStatus.initiated,
        ExecutionStatus.scored,
        ExecutionStatus.route_selected,
        ExecutionStatus.executing,
        ExecutionStatus.completed,
    ]


# ── Uncertain outcomes ──
# Example: Rail asks a battery to discharge at 50 kW (±2 kW), then judges
# what the evidence supports. The rules are domain-neutral.

T0 = datetime(2026, 10, 16, 9, 0, tzinfo=timezone.utc)
S = ExecutionStatus


def _instr(target=50.0):
    return Instruction(id="cmd-1", resource="battery-1", session="boot-1",
                       target=target, tolerance=2.0, issued_at=T0,
                       settle_seconds=10, max_reading_age_seconds=60)


def _seen(receipt=None, reading=None, at_s=30, **identity):
    """Evidence correctly identified as being about cmd-1 unless overridden."""
    read_at = T0 + timedelta(seconds=at_s) if reading is not None else None
    fields = dict(instruction_id="cmd-1" if receipt else None,
                  resource="battery-1", session="boot-1")
    fields.update(identity)
    return Observation(receipt=receipt, reading=reading, read_at=read_at, **fields)


NOW = T0 + timedelta(seconds=40)


def _executing():
    state = create_execution("req-1", "route-1")
    for s in (S.scored, S.route_selected, S.executing):
        state = advance_state(state, s)
    return state


def test_accepted_and_reading_within_tolerance_completes():
    state = record_outcome(_executing(), _instr(), _seen(Receipt.accepted, 49.1), NOW)
    assert state.status == S.completed
    assert "within ±2.0" in state.assessments[-1]["reason"]


def test_accepted_but_output_unchanged_is_mismatch_not_success():
    state = record_outcome(_executing(), _instr(), _seen(Receipt.accepted, 0.0), NOW)
    assert state.status == S.mismatched


def test_connection_lost_after_send_is_uncertain():
    state = record_outcome(_executing(), _instr(), _seen(None, None), NOW)
    assert state.status == S.uncertain
    assert state.completed_at is None


def test_missing_reading_is_never_zero():
    # Target 0 kW: substituting zero for a missing reading would falsely confirm.
    state = record_outcome(_executing(), _instr(target=0.0),
                           _seen(Receipt.accepted, None), NOW)
    assert state.status == S.uncertain


def test_stale_reading_does_not_count():
    old = _seen(Receipt.accepted, 50.0, at_s=30)
    verdict = assess(_instr(), old, now=T0 + timedelta(seconds=200))
    assert verdict.outcome == S.uncertain and "stale" in verdict.reason


def test_reading_before_settle_time_does_not_count():
    verdict = assess(_instr(), _seen(Receipt.accepted, 0.0, at_s=5), NOW)
    assert verdict.outcome == S.uncertain and not verdict.reading_usable


def test_no_receipt_cannot_claim_success_even_if_reading_matches():
    verdict = assess(_instr(), _seen(None, 50.0), NOW)
    assert verdict.outcome == S.uncertain and "cannot be attributed" in verdict.reason


def test_rejected_fails():
    state = record_outcome(_executing(), _instr(), _seen(Receipt.rejected), NOW)
    assert state.status == S.failed


def test_not_found_with_effect_present_is_still_uncertain():
    verdict = assess(_instr(), _seen(Receipt.not_found, 50.0), NOW)
    assert verdict.outcome == S.uncertain and "not proof" in verdict.reason


def test_reconcile_lost_acknowledgement_completes():
    state = record_outcome(_executing(), _instr(), _seen(None, None), NOW)
    later = NOW + timedelta(seconds=20)
    state = reconcile(state, _instr(), _seen(Receipt.accepted, 50.4, at_s=55), later)
    assert state.status == S.completed
    assert [a["kind"] for a in state.assessments] == ["outcome", "reconciliation"]


def test_reconcile_fenced_non_execution_fails_and_allows_reissue():
    state = record_outcome(_executing(), _instr(), _seen(None, None), NOW)
    assert safe_to_reissue(state) is False
    state = reconcile(state, _instr(),
                      _seen(Receipt.fenced_no_execution, 0.0, at_s=35), NOW)
    assert state.status == S.failed
    assert safe_to_reissue(state) is True


def test_inconclusive_reconcile_stays_uncertain_and_is_recorded():
    state = record_outcome(_executing(), _instr(), _seen(None, None), NOW)
    state = reconcile(state, _instr(), _seen(None, None), NOW)
    assert state.status == S.uncertain
    assert len(state.assessments) == 2
    assert safe_to_reissue(state) is False


def test_cannot_reconcile_a_settled_outcome():
    state = record_outcome(_executing(), _instr(), _seen(Receipt.accepted, 50.0), NOW)
    with pytest.raises(ValueError):
        reconcile(state, _instr(), _seen(Receipt.accepted, 50.0), NOW)


def test_uncertain_cannot_be_forced_back_to_executing():
    state = record_outcome(_executing(), _instr(), _seen(None, None), NOW)
    with pytest.raises(ValueError):
        advance_state(state, S.executing)


def test_same_evidence_same_verdict():
    a = assess(_instr(), _seen(Receipt.accepted, 49.0), NOW)
    b = assess(_instr(), _seen(Receipt.accepted, 49.0), NOW)
    assert a == b


# ── Regressions (found in review, 2026-10-16) ──

def test_rejected_with_effect_present_is_contradiction_not_failure():
    state = record_outcome(_executing(), _instr(), _seen(Receipt.rejected, 50.0), NOW)
    assert state.status == S.uncertain
    assert "contradictory" in state.assessments[-1]["reason"]
    assert safe_to_reissue(state) is False


def test_advance_state_cannot_bypass_reconciliation():
    state = record_outcome(_executing(), _instr(), _seen(None, None), NOW)
    with pytest.raises(ValueError):
        advance_state(state, S.failed)
    assert state.status == S.uncertain
    assert safe_to_reissue(state) is False


def test_failure_set_without_evidence_does_not_permit_reissue():
    state = advance_state(_executing(), S.failed)
    assert safe_to_reissue(state) is False


# ── Regressions (found in textbook review, 2026-10-17; textbook 06-19, 06-30) ──

def test_not_found_alone_does_not_permit_reissue():
    # The instruction may be delayed, queued elsewhere, or forgotten after a restart.
    state = record_outcome(_executing(), _instr(), _seen(None, None), NOW)
    state = reconcile(state, _instr(), _seen(Receipt.not_found, 0.0, at_s=35), NOW)
    assert state.status == S.uncertain
    assert safe_to_reissue(state) is False


def test_fenced_with_effect_present_is_contradiction_not_failure():
    verdict = assess(_instr(), _seen(Receipt.fenced_no_execution, 50.0), NOW)
    assert verdict.outcome == S.uncertain and "contradictory" in verdict.reason


def test_receipt_for_another_instruction_is_not_evidence():
    verdict = assess(_instr(), _seen(Receipt.accepted, 50.0, instruction_id="cmd-old"), NOW)
    assert verdict.outcome == S.uncertain and "cmd-old" in verdict.reason


def test_reading_from_another_resource_does_not_count():
    verdict = assess(_instr(), _seen(Receipt.accepted, 50.0, resource="battery-2"), NOW)
    assert verdict.outcome == S.uncertain and not verdict.reading_usable


def test_evidence_from_a_new_device_session_is_uncertain():
    # Accepted before a restart; the device now reports from a new boot.
    verdict = assess(_instr(), _seen(Receipt.accepted, 50.0, session="boot-2"), NOW)
    assert verdict.outcome == S.uncertain and "restarted" in verdict.reason


# ── Website ──

def test_website_rules_file_matches_code():
    # website/assets/rail-rules.json must be regenerated whenever the rules change:
    #   PYTHONPATH=. python scripts/build_rail_rules.py
    import json
    from scripts.build_rail_rules import OUT, build
    assert json.loads(OUT.read_text(encoding="utf-8")) == build()
