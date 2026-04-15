"""
Rail-lite Executor — state machine for payment execution simulation.
States: initiated → scored → route_selected → executing → completed/failed

From P3-Ch2/Ch3: execution pipeline, settlement, retry, state machines.
"""
from datetime import datetime
from src.models.schemas import ExecutionState, ExecutionStatus


def create_execution(request_id: str, route_id: str) -> ExecutionState:
    """Create a new execution in initiated state."""
    state = ExecutionState(
        request_id=request_id,
        route_id=route_id,
        status=ExecutionStatus.initiated,
        started_at=datetime.utcnow(),
    )
    state.state_history.append({
        "from": None,
        "to": ExecutionStatus.initiated,
        "timestamp": datetime.utcnow().isoformat(),
    })
    return state


def advance_state(state: ExecutionState, to_status: ExecutionStatus) -> ExecutionState:
    """
    Advance the execution to the next state.
    V0: deterministic progression (no real failures).
    Future: actual hop-level execution with retry logic.
    """
    valid_transitions = {
        ExecutionStatus.initiated:      [ExecutionStatus.scored],
        ExecutionStatus.scored:         [ExecutionStatus.route_selected],
        ExecutionStatus.route_selected: [ExecutionStatus.executing],
        ExecutionStatus.executing:      [ExecutionStatus.completed, ExecutionStatus.failed],
    }

    allowed = valid_transitions.get(state.status, [])
    if to_status not in allowed:
        raise ValueError(
            f"Invalid transition: {state.status} → {to_status}. "
            f"Allowed: {allowed}"
        )

    state.state_history.append({
        "from": state.status,
        "to": to_status,
        "timestamp": datetime.utcnow().isoformat(),
    })
    state.status = to_status

    if to_status in (ExecutionStatus.completed, ExecutionStatus.failed):
        state.completed_at = datetime.utcnow()

    return state


def simulate_full_execution(request_id: str, route_id: str) -> ExecutionState:
    """
    Run the full state machine: initiated → scored → route_selected → executing → completed.
    V0: always succeeds. Future: failure simulation based on reliability score.
    """
    state = create_execution(request_id, route_id)
    for next_status in [
        ExecutionStatus.scored,
        ExecutionStatus.route_selected,
        ExecutionStatus.executing,
        ExecutionStatus.completed,
    ]:
        state = advance_state(state, next_status)
    return state
