"""
Rail-lite Executor — state machine for payment execution simulation.
States: initiated → scored → route_selected → executing → completed/failed
        executing → mismatched | uncertain
        uncertain → completed | failed | mismatched   (only via reconcile)

From P3-Ch2/Ch3: execution pipeline, settlement, retry, state machines.
Outcome rules live in outcome.py.
"""
from datetime import datetime
from src.models.schemas import (
    ExecutionState, ExecutionStatus, Instruction, Observation,
)
from src.rail_lite.outcome import assess

TERMINAL = (ExecutionStatus.completed, ExecutionStatus.failed, ExecutionStatus.mismatched)


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

    An uncertain execution cannot be moved from here: only reconcile(),
    with new evidence, may resolve it.
    """
    if state.status == ExecutionStatus.uncertain:
        raise ValueError(
            "An uncertain outcome can only be resolved by reconcile() with new evidence"
        )
    return _transition(state, to_status)


def _transition(state: ExecutionState, to_status: ExecutionStatus) -> ExecutionState:
    """Validated state change. Callers decide whether evidence is required."""
    valid_transitions = {
        ExecutionStatus.initiated: [ExecutionStatus.scored],
        ExecutionStatus.scored: [ExecutionStatus.route_selected],
        ExecutionStatus.route_selected: [ExecutionStatus.executing],
        ExecutionStatus.executing: [
            ExecutionStatus.completed, ExecutionStatus.failed,
            ExecutionStatus.mismatched, ExecutionStatus.uncertain,
        ],
        ExecutionStatus.uncertain: [
            ExecutionStatus.completed, ExecutionStatus.failed,
            ExecutionStatus.mismatched,
        ],
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

    if to_status in TERMINAL:
        state.completed_at = datetime.utcnow()

    return state


def record_outcome(state: ExecutionState, instruction: Instruction,
                   observation: Observation, now: datetime) -> ExecutionState:
    """
    First verdict after the instruction is sent: executing → one of
    completed / failed / mismatched / uncertain, decided by the evidence.
    """
    if state.status != ExecutionStatus.executing:
        raise ValueError(f"Can only record an outcome while executing, not {state.status}")
    verdict = assess(instruction, observation, now, kind="outcome")
    state.assessments.append(verdict.model_dump(mode="json"))
    return _transition(state, verdict.outcome)


def reconcile(state: ExecutionState, instruction: Instruction,
              observation: Observation, now: datetime) -> ExecutionState:
    """
    Resolve an uncertain outcome with fresh evidence — typically a status
    query to the counterparty plus a new reading.

    If the evidence is still inconclusive the state stays uncertain and the
    attempt is recorded. Rail never upgrades uncertainty to success by default.
    """
    if state.status != ExecutionStatus.uncertain:
        raise ValueError(f"Can only reconcile an uncertain outcome, not {state.status}")
    verdict = assess(instruction, observation, now, kind="reconciliation")
    state.assessments.append(verdict.model_dump(mode="json"))
    if verdict.outcome != ExecutionStatus.uncertain:
        state = _transition(state, verdict.outcome)
    return state


def safe_to_reissue(state: ExecutionState) -> bool:
    """
    May the same instruction be sent again? Only once an evidence verdict
    has established it failed. While uncertain the first one may already
    have taken effect, and sending again risks doing it twice. A failure
    set by hand, with no assessment behind it, does not count.
    """
    return (state.status == ExecutionStatus.failed
            and bool(state.assessments)
            and state.assessments[-1]["outcome"] == ExecutionStatus.failed.value)


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
