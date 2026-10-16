#!/usr/bin/env python3
"""
Lupine — Rail uncertain-outcome demo.

Rail sends an instruction to a pretend battery controller, then decides what
the evidence actually supports. The controller has switches that make it
misbehave, so every case Rail must handle can be seen in one run.

SIMULATED. SimulatedBattery models no real device, protocol or register map.
It exists only to exercise Rail's rules (src/rail_lite/outcome.py). Whether a
real integration works can only be established against real equipment.

Run:  PYTHONPATH=. python scripts/rail_uncertainty_demo.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.schemas import ExecutionStatus, Instruction, Observation, Receipt
from src.rail_lite.executor import (
    advance_state, create_execution, record_outcome, reconcile, safe_to_reissue,
)
from src.cloked_lite.logger import append_evidence, create_evidence_log, verify_chain

T0 = datetime(2026, 10, 16, 9, 0, tzinfo=timezone.utc)   # fixed clock: same run, same output


class SimulatedBattery:
    """A pretend controller. Each switch breaks one thing."""

    def __init__(self, *, loses_instruction=False, rejects=False, ignores=False,
                 reply_lost=False, sensor_down=False):
        self.loses_instruction = loses_instruction
        self.rejects = rejects
        self.ignores = ignores
        self.reply_lost = reply_lost
        self.sensor_down = sensor_down
        self.output_kw = 0.0
        self.records: dict[str, Receipt] = {}

    def send(self, instr: Instruction) -> Optional[Receipt]:
        if self.loses_instruction:
            return None                                  # never arrived
        receipt = Receipt.rejected if self.rejects else Receipt.accepted
        self.records[instr.id] = receipt
        if receipt is Receipt.accepted and not self.ignores:
            self.output_kw = instr.target
        return None if self.reply_lost else receipt

    def status(self, instr_id: str) -> Receipt:
        return self.records.get(instr_id, Receipt.not_found)

    def read(self, at: datetime) -> tuple[Optional[float], Optional[datetime]]:
        return (None, None) if self.sensor_down else (self.output_kw, at)


SCENARIOS = [
    ("Healthy controller",               50.0, {}),
    ("Accepts, but output never moves",  50.0, {"ignores": True}),
    ("Reply lost — it actually worked",  50.0, {"reply_lost": True}),
    ("Reply lost — it was refused",      50.0, {"reply_lost": True, "rejects": True}),
    ("Instruction lost in transit",      50.0, {"loses_instruction": True}),
    ("Stop discharging, sensor down",     0.0, {"sensor_down": True}),
]


def run_one(title: str, target: float, faults: dict) -> tuple[ExecutionStatus, bool]:
    battery = SimulatedBattery(**faults)
    instr = Instruction(id="cmd-1", target=target, tolerance=2.0, issued_at=T0,
                        settle_seconds=10, max_reading_age_seconds=60)
    state = create_execution("demo", "battery-1")
    for s in (ExecutionStatus.scored, ExecutionStatus.route_selected, ExecutionStatus.executing):
        state = advance_state(state, s)
    log = create_evidence_log("demo")
    log = append_evidence(log, "instruction_issued", instr.model_dump(mode="json"))

    receipt = battery.send(instr)
    value, at = battery.read(T0 + timedelta(seconds=15))
    state = record_outcome(state, instr, Observation(receipt=receipt, reading=value, read_at=at),
                           now=T0 + timedelta(seconds=20))
    log = append_evidence(log, "outcome_assessed", state.assessments[-1])

    if state.status == ExecutionStatus.uncertain:
        value, at = battery.read(T0 + timedelta(seconds=55))
        state = reconcile(state, instr,
                          Observation(receipt=battery.status(instr.id), reading=value, read_at=at),
                          now=T0 + timedelta(seconds=60))
        log = append_evidence(log, "reconciliation_attempted", state.assessments[-1])

    print(f"\n  {title}")
    print(f"    asked for {target} kW (±{instr.tolerance})")
    for a in state.assessments:
        label = "first look" if a["kind"] == "outcome" else "reconcile "
        print(f"    {label} → {a['outcome'].upper():<10} {a['reason']}")
    print(f"    safe to send again: {'yes' if safe_to_reissue(state) else 'no'}")
    return state.status, verify_chain(log)


def main() -> int:
    print("Lupine · Rail uncertain-outcome demo  [SIMULATED controller]")
    results = [run_one(*s) for s in SCENARIOS]
    all_valid = all(ok for _, ok in results)
    print(f"\n  Evidence chains: {len(results)} written, "
          f"{'all verify' if all_valid else 'VERIFICATION FAILED'}.")
    print("  What that proves: none of these records was altered afterwards.")
    print("  What it does not prove: that any reading was accurate.")
    return 0 if all_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
