#!/usr/bin/env python3
"""
Lupine Systems V0 — Daily Live Decisions

Fetches today's live AUD/SGD rate from Frankfurter, runs the full
decision engine for every urgency level, and writes the results
(including CLOKED evidence hashes) to website/data/live_decisions.json.

Called by daily.yml after tests pass. The website reads this file
directly — no separate API server needed.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.schemas import MovementRequest, Urgency
from src.aiva_lite.router import generate_routes
from src.aiva_lite.scorer import score_routes
from src.aiva_lite.selector import select_route
from src.cloked_lite.logger import create_evidence_log, append_evidence, verify_chain
from src.data.fx_feed import fetch_fx_rate

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH  = REPO_ROOT / "website" / "data" / "live_decisions.json"

AMOUNT   = 500_000
FROM_CCY = "AUD"
TO_CCY   = "SGD"


def fetch_live_rate() -> tuple[float, str, str]:
    fx = fetch_fx_rate(FROM_CCY, TO_CCY)
    return float(fx["rate"]), fx.get("date", ""), fx.get("source", "unknown")


def run_decision(fx_rate: float, urgency: Urgency) -> dict:
    req = MovementRequest(
        amount=AMOUNT,
        from_currency=FROM_CCY,
        to_currency=TO_CCY,
        urgency=urgency,
    )

    routes           = generate_routes(req, fx_rate=fx_rate)
    scored, weights  = score_routes(routes, urgency)
    decision         = select_route(req.id, scored, weights)

    # Build evidence chain
    evidence = create_evidence_log(req.id)
    evidence = append_evidence(evidence, "request_created",  req.model_dump(mode="json"))
    evidence = append_evidence(evidence, "fx_observed",      {"rate": fx_rate, "date": datetime.utcnow().isoformat()})
    evidence = append_evidence(evidence, "routes_scored",    decision.model_dump(mode="json"))

    winner = next(r for r in scored if r.id == decision.selected_route_id)
    bank   = next((r for r in scored if r.name == "Bank SWIFT"), scored[-1])
    saving = AMOUNT * (bank.estimated_cost_bps - winner.estimated_cost_bps) / 10_000

    return {
        "selected":        winner.name,
        "corridor":        winner.corridor,
        "time_hours":      winner.estimated_time_hours,
        "cost_bps":        winner.estimated_cost_bps,
        "composite_score": round(winner.composite_score, 3),
        "saving_vs_bank":  round(saving, 2),
        "rationale":       decision.rationale,
        "weights":         weights,
        "all_routes": [
            {
                "name":      r.name,
                "speed":     round(r.speed_score, 3),
                "cost":      round(r.cost_score, 3),
                "reliability": round(r.reliability_score, 3),
                "composite": round(r.composite_score, 3),
                "cost_bps":  r.estimated_cost_bps,
                "time_hours": r.estimated_time_hours,
            }
            for r in scored
        ],
        "evidence_hash":  evidence.entries[-1].data_hash,
        "chain_valid":    verify_chain(evidence),
        "request_id":     req.id,
    }


def main() -> int:
    print("Fetching live AUD/SGD rate…")
    try:
        fx_rate, fx_date, fx_source = fetch_live_rate()
    except Exception as e:
        # Frankfurter is occasionally unreachable in CI. Keep the last good
        # file rather than failing the whole workflow with a network blip.
        print(f"WARNING: Frankfurter API unreachable — {e}")
        if OUT_PATH.exists():
            print("Keeping existing live_decisions.json unchanged.")
        else:
            print("No prior live_decisions.json to preserve — site will show stale data.")
        return 0

    print(f"Rate: 1 AUD = {fx_rate} SGD ({fx_date})")

    decisions = {}
    for urg in Urgency:
        d = run_decision(fx_rate, urg)
        decisions[urg.value] = d
        print(f"  {urg.value:10} → {d['selected']:12}  "
              f"score={d['composite_score']}  save=A${d['saving_vs_bank']:,.0f}  "
              f"hash={d['evidence_hash'][:16]}…")

    output = {
        "generated":    datetime.utcnow().isoformat()[:19] + "Z",
        "date":         fx_date,
        "fx_rate":      fx_rate,
        "fx_source":    fx_source,
        "amount":       AMOUNT,
        "corridor":     f"{FROM_CCY}/{TO_CCY}",
        "decisions":    decisions,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, indent=2))
    print(f"Saved → {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
