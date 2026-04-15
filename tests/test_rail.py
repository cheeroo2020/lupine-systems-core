"""Tests for Rail-lite: state machine execution."""
import pytest
from src.rail_lite.executor import create_execution, advance_state, simulate_full_execution
from src.models.schemas import ExecutionStatus


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
