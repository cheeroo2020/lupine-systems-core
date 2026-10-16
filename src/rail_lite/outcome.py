"""
Rail-lite Outcome — what can honestly be said after an instruction is sent.

An instruction can be sent and then nothing heard back. In that moment there
are three different worlds — it never arrived, it was refused, or it took
effect and the reply was lost — and they look identical from the sender's
side. Rail must not pick one. These rules decide what the evidence supports:

  1. completed   needs BOTH: the counterparty accepted the instruction,
                 AND a usable reading shows the effect within tolerance.
  2. failed      needs the counterparty to say it refused the instruction,
                 or that it never received it — and no usable reading showing
                 the effect anyway. Contradictory evidence stays uncertain.
  3. mismatched  the counterparty accepted, but a usable reading disagrees.
                 Not success.
  4. uncertain   anything else. A missing reading is never zero, and a
                 reading that is stale, too early, or from the future does
                 not count.
  5. While uncertain, the instruction must not be sent again, and only
     reconcile() with new evidence can leave uncertain — see executor.py.

assess() is a pure function of (instruction, observation, now): the same
evidence always gives the same verdict, and the reason is recorded with it.

Domain-neutral on purpose. `target` can be a battery setpoint in kW or an
amount credited to a beneficiary; Rail only needs the number and the rules.
"""
import math
from datetime import datetime, timedelta
from src.models.schemas import (
    Assessment, ExecutionStatus, Instruction, Observation, Receipt,
)


def reading_usable(instruction: Instruction, observation: Observation,
                   now: datetime) -> tuple[bool, str]:
    """Can this reading be used to judge the instruction's effect?"""
    value, read_at = observation.reading, observation.read_at
    if value is None or read_at is None:
        return False, "no reading available"
    if math.isnan(value):
        return False, "reading is not a number"
    if read_at > now:
        return False, "reading timestamp is in the future"

    earliest = instruction.issued_at + timedelta(seconds=instruction.settle_seconds)
    if read_at < earliest:
        return False, "reading taken before the instruction could take effect"

    age = (now - read_at).total_seconds()
    if age > instruction.max_reading_age_seconds:
        return False, (f"reading is stale ({age:.0f}s old, "
                       f"limit {instruction.max_reading_age_seconds:.0f}s)")
    return True, "reading usable"


def assess(instruction: Instruction, observation: Observation, now: datetime,
           kind: str = "outcome") -> Assessment:
    """Turn evidence into a verdict. Never assumes what was not observed."""
    usable, why = reading_usable(instruction, observation, now)
    within = usable and abs(observation.reading - instruction.target) <= instruction.tolerance
    receipt = observation.receipt
    met = (f"reading {observation.reading} within ±{instruction.tolerance} "
           f"of target {instruction.target}")
    missed = (f"reading {observation.reading} outside ±{instruction.tolerance} "
              f"of target {instruction.target}")

    if receipt in (Receipt.rejected, Receipt.not_found):
        said = ("rejected the instruction" if receipt is Receipt.rejected
                else "has no record of the instruction")
        if within:
            outcome, reason = ExecutionStatus.uncertain, (
                f"counterparty {said}, yet {met} — contradictory evidence")
        elif receipt is Receipt.rejected:
            outcome, reason = ExecutionStatus.failed, f"counterparty {said}"
        else:
            outcome, reason = ExecutionStatus.failed, f"counterparty {said} — it never arrived"
    elif receipt is None and within:
        outcome, reason = ExecutionStatus.uncertain, (
            f"no receipt; {met}, but the effect cannot be attributed "
            "to this instruction")
    elif receipt is None:
        outcome, reason = ExecutionStatus.uncertain, f"no receipt; {missed if usable else why}"
    elif not usable:
        outcome, reason = ExecutionStatus.uncertain, f"accepted, but {why}"
    elif within:
        outcome, reason = ExecutionStatus.completed, f"accepted and {met}"
    else:
        outcome, reason = ExecutionStatus.mismatched, f"accepted, but {missed}"

    return Assessment(
        instruction_id=instruction.id,
        kind=kind,
        outcome=outcome,
        reason=reason,
        receipt=receipt,
        reading=observation.reading,
        read_at=observation.read_at,
        reading_usable=usable,
        assessed_at=now,
    )
