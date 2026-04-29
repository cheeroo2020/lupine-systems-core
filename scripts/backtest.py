#!/usr/bin/env python3
"""
Lupine Systems V0 — Historical Backtest

Fetches 90 days of AUD/SGD rates from Frankfurter (ECB reference),
runs the full decision engine on each trading day for all urgency levels,
and computes cumulative savings vs. always using a bank SWIFT transfer.

Writes website/data/backtest.json for the dashboard.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.schemas import MovementRequest, Urgency
from src.aiva_lite.router import generate_routes
from src.aiva_lite.scorer import score_routes
from src.aiva_lite.selector import select_route

REPO_ROOT  = Path(__file__).resolve().parent.parent
OUT_PATH   = REPO_ROOT / "website" / "data" / "backtest.json"

AMOUNT      = 500_000
FROM_CCY    = "AUD"
TO_CCY      = "SGD"
LOOKBACK    = 90    # trading days to fetch
URGENCIES   = [Urgency.low, Urgency.normal, Urgency.high, Urgency.critical]


# ── Fetch historical rates ────────────────────────────────────────────

def fetch_rates(lookback_days: int = LOOKBACK) -> dict[str, float]:
    end   = date.today()
    start = end - timedelta(days=lookback_days + 30)   # extra buffer for weekends
    url   = (
        f"https://api.frankfurter.app/{start}..{end}"
        f"?from={FROM_CCY}&to={TO_CCY}"
    )
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    raw = r.json().get("rates", {})
    # sort ascending, keep last LOOKBACK trading days
    sorted_dates = sorted(raw.keys())
    trimmed = sorted_dates[-lookback_days:]
    return {d: raw[d][TO_CCY] for d in trimmed}


# ── Engine run for one day ────────────────────────────────────────────

def run_one_day(fx_rate: float, urgency: Urgency):
    req = MovementRequest(
        amount=AMOUNT,
        from_currency=FROM_CCY,
        to_currency=TO_CCY,
        urgency=urgency,
    )
    routes         = generate_routes(req, fx_rate=fx_rate)
    scored, weights = score_routes(routes, urgency)
    decision       = select_route(req.id, scored, weights)

    winner = next(r for r in scored if r.id == decision.selected_route_id)
    bank   = next((r for r in scored if r.name == "Bank SWIFT"), scored[-1])

    winner_cost_aud = AMOUNT * winner.estimated_cost_bps / 10_000
    bank_cost_aud   = AMOUNT * bank.estimated_cost_bps   / 10_000
    saving_aud      = bank_cost_aud - winner_cost_aud

    return {
        "selected":    winner.name,
        "cost_bps":    winner.estimated_cost_bps,
        "composite":   round(winner.composite_score, 3),
        "saving_aud":  round(saving_aud, 2),
        "bank_cost":   round(bank_cost_aud, 2),
    }


# ── Backtest ──────────────────────────────────────────────────────────

def run_backtest(rates: dict[str, float]) -> dict:
    days_rows = []

    # per-urgency accumulators
    totals = {u.value: {"saving": 0.0, "bank_cost": 0.0, "wins": {}} for u in URGENCIES}

    for date_str, rate in rates.items():
        row: dict = {"date": date_str, "rate": round(rate, 5), "decisions": {}}

        for urg in URGENCIES:
            d = run_one_day(rate, urg)
            u = urg.value
            totals[u]["saving"]    += d["saving_aud"]
            totals[u]["bank_cost"] += d["bank_cost"]
            totals[u]["wins"][d["selected"]] = totals[u]["wins"].get(d["selected"], 0) + 1
            row["decisions"][u] = d

        days_rows.append(row)

    n = len(rates)
    summary = {}
    for u, t in totals.items():
        summary[u] = {
            "total_saving_aud":           round(t["saving"], 2),
            "avg_saving_per_transfer":    round(t["saving"] / n, 2) if n else 0,
            "bank_total_cost_aud":        round(t["bank_cost"], 2),
            "n_days":                     n,
            "provider_wins":              t["wins"],
        }

    return {
        "generated":   datetime.utcnow().isoformat()[:10],
        "corridor":    f"{FROM_CCY}/{TO_CCY}",
        "amount":      AMOUNT,
        "n_days":      n,
        "rate_range":  {
            "min": round(min(rates.values()), 5),
            "max": round(max(rates.values()), 5),
        },
        "summary":     summary,
        "days":        days_rows,
    }


# ── Entry point ───────────────────────────────────────────────────────

def main() -> int:
    print(f"Fetching {LOOKBACK} trading days of {FROM_CCY}/{TO_CCY} rates…")
    try:
        rates = fetch_rates()
    except Exception as e:
        print(f"ERROR: could not fetch rates — {e}")
        return 1

    print(f"Got {len(rates)} days ({list(rates.keys())[0]} → {list(rates.keys())[-1]})")

    result = run_backtest(rates)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(result, indent=2))
    print(f"Saved → {OUT_PATH}")

    # Print quick summary
    print()
    print(f"{'Urgency':10} {'Avg saving/transfer':>22}  {'Provider wins'}")
    print("─" * 65)
    for u, s in result["summary"].items():
        wins_str = ", ".join(f"{k} {v}×" for k, v in s["provider_wins"].items())
        print(f"{u:10} A${s['avg_saving_per_transfer']:>18,.0f}  {wins_str}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
