#!/usr/bin/env python3
"""
Lupine — export Rail's verdicts for the website's "Try the rules" panel.

Runs the real record_outcome() and safe_to_reissue() from src/rail_lite over
every combination the page offers, and writes the results to
website/assets/rail-rules.json. The page only looks results up and holds no
copy of the rules, so it cannot drift from the code: tests/test_rail.py fails
if this file is out of date.

Example used throughout: Rail asked a battery for 50 kW (±2 kW).

Run:  PYTHONPATH=. python scripts/build_rail_rules.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.schemas import ExecutionStatus, Instruction, Observation, Receipt
from src.rail_lite.executor import (
    advance_state, create_execution, record_outcome, safe_to_reissue,
)

OUT = Path(__file__).resolve().parent.parent / "website" / "assets" / "rail-rules.json"

T0 = datetime(2026, 1, 1, tzinfo=timezone.utc)   # arbitrary fixed clock
NOW = T0 + timedelta(seconds=100)

RECEIPTS = {
    "none": None,
    "accepted": Receipt.accepted,
    "rejected": Receipt.rejected,
    "not_found": Receipt.not_found,
    "fenced": Receipt.fenced_no_execution,
}
READINGS = {                      # (value in kW, seconds after the instruction)
    "none": None,
    "at_target": (50.0, 95),      # fresh: 5 s old
    "off_target": (0.0, 95),
    "old": (50.0, 20),            # 80 s old; the limit is 60 s
}
IDENTITY = {
    "this": {},
    "other_instruction": {"instruction_id": "cmd-old"},
    "restarted": {"session": "boot-2"},
}


def verdict(receipt_key: str, reading_key: str, identity_key: str) -> dict:
    instruction = Instruction(id="cmd-1", resource="battery-1", session="boot-1",
                              target=50.0, tolerance=2.0, issued_at=T0,
                              settle_seconds=10, max_reading_age_seconds=60)
    receipt, reading = RECEIPTS[receipt_key], READINGS[reading_key]
    fields = dict(receipt=receipt,
                  instruction_id="cmd-1" if receipt else None,
                  resource="battery-1", session="boot-1")
    if reading:
        fields.update(reading=reading[0], read_at=T0 + timedelta(seconds=reading[1]))
    for key, value in IDENTITY[identity_key].items():
        if key != "instruction_id" or receipt:
            fields[key] = value
    state = create_execution("website", "battery-1")
    for status in (ExecutionStatus.scored, ExecutionStatus.route_selected,
                   ExecutionStatus.executing):
        state = advance_state(state, status)
    state = record_outcome(state, instruction, Observation(**fields), NOW)
    return {"verdict": state.status.value,
            "reason": state.assessments[-1]["reason"],
            "safe_to_resend": safe_to_reissue(state)}


def build() -> dict:
    results = {f"{r}|{s}|{i}": verdict(r, s, i)
               for r in RECEIPTS for s in READINGS for i in IDENTITY}
    return {
        "generated_from": "src/rail_lite/outcome.py and executor.py",
        "example": "Rail asked a battery for 50 kW (±2 kW); readings older than 60 s are stale",
        "results": results,
    }


def main() -> int:
    OUT.write_text(json.dumps(build(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(OUT.parents[2])} ({len(build()['results'])} combinations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
