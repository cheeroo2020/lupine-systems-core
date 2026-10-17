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

    resource = "battery-1"

    def __init__(self, *, loses_instruction=False, rejects=False, ignores=False,
                 reply_lost=False, sensor_down=False, initial_kw=0.0,
                 fences=False, restarts=False):
        self.loses_instruction = loses_instruction
        self.rejects = rejects
        self.ignores = ignores
        self.reply_lost = reply_lost or restarts
        self.sensor_down = sensor_down
        self.fences = fences          # can guarantee an unknown instruction never runs
        self.restarts = restarts      # reboots right after acting; its records are lost
        self.output_kw = initial_kw
        self.session = "boot-1"
        self.records: dict[str, Receipt] = {}

    def send(self, instr: Instruction) -> Optional[Receipt]:
        if self.loses_instruction:
            return None                                  # never arrived
        receipt = Receipt.rejected if self.rejects else Receipt.accepted
        self.records[instr.id] = receipt
        if receipt is Receipt.accepted and not self.ignores:
            self.output_kw = instr.target
        if self.restarts:
            self.session, self.records = "boot-2", {}    # volatile history is gone
        return None if self.reply_lost else receipt

    def status(self, instr_id: str) -> Receipt:
        if instr_id in self.records:
            return self.records[instr_id]
        return Receipt.fenced_no_execution if self.fences else Receipt.not_found

    def observe(self, instr_id: str, receipt: Optional[Receipt], at: datetime) -> Observation:
        """Evidence as the device reports it, labelled with what it is about."""
        value, read_at = (None, None) if self.sensor_down else (self.output_kw, at)
        return Observation(receipt=receipt, instruction_id=instr_id if receipt else None,
                           reading=value, read_at=read_at,
                           resource=self.resource, session=self.session)


SCENARIOS = [
    ("Healthy controller",               50.0, {}),
    ("Accepts, but output never moves",  50.0, {"ignores": True}),
    ("Reply lost — it actually worked",  50.0, {"reply_lost": True}),
    ("Reply lost — it was refused",      50.0, {"reply_lost": True, "rejects": True}),
    ("Lost; device can only say not found", 50.0, {"loses_instruction": True}),
    ("Lost; device guarantees it never ran", 50.0, {"loses_instruction": True, "fences": True}),
    ("Accepted, then the device restarted", 50.0, {"restarts": True}),
    ("Stop discharging, sensor down",     0.0, {"sensor_down": True}),
    ("Refuses, yet output already there", 50.0, {"rejects": True, "initial_kw": 50.0}),
]


def run_one(title: str, target: float, faults: dict) -> tuple[ExecutionStatus, bool]:
    battery = SimulatedBattery(**faults)
    instr = Instruction(id="cmd-1", resource=battery.resource, session=battery.session,
                        target=target, tolerance=2.0, issued_at=T0,
                        settle_seconds=10, max_reading_age_seconds=60)
    state = create_execution("demo", "battery-1")
    for s in (ExecutionStatus.scored, ExecutionStatus.route_selected, ExecutionStatus.executing):
        state = advance_state(state, s)
    log = create_evidence_log("demo")
    log = append_evidence(log, "instruction_issued", instr.model_dump(mode="json"))

    receipt = battery.send(instr)
    state = record_outcome(state, instr,
                           battery.observe(instr.id, receipt, T0 + timedelta(seconds=15)),
                           now=T0 + timedelta(seconds=20))
    log = append_evidence(log, "outcome_assessed", state.assessments[-1])

    if state.status == ExecutionStatus.uncertain:
        state = reconcile(state, instr,
                          battery.observe(instr.id, battery.status(instr.id),
                                          T0 + timedelta(seconds=55)),
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
    print("  What that proves: each record is consistent with the ones before it.")
    print("  It catches a rewrite only against a copy of the final hash kept")
    print("  elsewhere (not built yet). It does not prove any reading was accurate.")
    return 0 if all_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
