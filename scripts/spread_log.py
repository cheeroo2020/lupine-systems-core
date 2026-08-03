#!/usr/bin/env python3
"""
Lupine — daily spread log.

Records one observation per run, append-only, so that after enough runs
there is a real dataset to cite instead of an illustrative one.

The central design rule: every number carries its own method.

    measured  — observed directly from a named source at a stated time
    modelled  — computed from a constant we chose
    derived   — arithmetic over measured values only

Nothing in this file may present a modelled number as a measured one.
That distinction is the whole reason the file exists.

WHAT IS ACTUALLY MEASURED HERE
    The disagreement between four independent public mid-market sources
    queried at the same instant. This is a genuine observable and, as far
    as we know, nobody publishes it for AUD/SGD.

WHAT IS NOT MEASURED
    Provider effective rates. We hold no quote API for Wise, Airwallex,
    OFX or any bank. Their basis points are constants in router.py whose
    provenance is a source comment, not a citation. They are written to
    the log flagged `modelled` and must not be quoted as observations.

Run:  PYTHONPATH=. python scripts/spread_log.py
"""
from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.fx_feed import fetch_all_sources
from src.models.schemas import MovementRequest, Urgency
from src.aiva_lite.router import generate_routes

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH  = REPO_ROOT / "website" / "data" / "spread_log.jsonl"
SUM_PATH  = REPO_ROOT / "website" / "data" / "spread_summary.json"

FROM_CCY, TO_CCY = "AUD", "SGD"
AMOUNT = 500_000


# ── observation ───────────────────────────────────────────────────────

def observe() -> dict:
    """One timestamped observation. Measured and modelled kept apart."""
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    sources = fetch_all_sources(FROM_CCY, TO_CCY)

    live = [s for s in sources if s.get("ok") and s.get("rate")]
    rates = [s["rate"] for s in live]

    measured: dict = {
        "method": "measured",
        "what": "disagreement between independent public mid-market sources, same instant",
        "n_sources_ok": len(live),
        "n_sources_tried": len(sources),
    }
    if len(rates) >= 2:
        lo, hi = min(rates), max(rates)
        mid = statistics.median(rates)
        measured.update({
            "min": round(lo, 6),
            "max": round(hi, 6),
            "median": round(mid, 6),
            "dispersion_bps": round((hi - lo) / mid * 10_000, 2),
            "stdev": round(statistics.stdev(rates), 6) if len(rates) > 2 else None,
        })
    elif len(rates) == 1:
        measured.update({"median": round(rates[0], 6), "dispersion_bps": None,
                         "note": "single source reachable — no dispersion observable"})
    else:
        measured.update({"median": None, "dispersion_bps": None,
                         "note": "no source reachable"})

    # Provider costs are constants, not quotes. Recorded, clearly fenced.
    modelled: dict = {
        "method": "modelled",
        "what": "provider cost in bps",
        "provenance": "hardcoded constants in src/aiva_lite/router.py; "
                      "source comment only, no citation, no retrieval date",
        "caution": "not a quote. must not be cited as an observation.",
        "providers": [],
    }
    if measured.get("median"):
        req = MovementRequest(amount=AMOUNT, from_currency=FROM_CCY,
                              to_currency=TO_CCY, urgency=Urgency.normal)
        for r in generate_routes(req, fx_rate=measured["median"]):
            modelled["providers"].append({
                "name": r.name,
                "bps": r.estimated_cost_bps,
                "hours": r.estimated_time_hours,
            })

    return {
        "ts": now,
        "pair": f"{FROM_CCY}/{TO_CCY}",
        "sources": [
            {"source": s.get("source"), "rate": s.get("rate"),
             "source_date": s.get("date", ""), "ok": s.get("ok", False)}
            for s in sources
        ],
        "measured": measured,
        "modelled": modelled,
    }


# ── accumulation ──────────────────────────────────────────────────────

def append(obs: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obs, separators=(",", ":")) + "\n")


def read_log() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    rows = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def summarise(rows: list[dict]) -> dict:
    """Only over measured values. Nothing modelled enters this."""
    disp = [r["measured"]["dispersion_bps"] for r in rows
            if r.get("measured", {}).get("dispersion_bps") is not None]

    # how often did each source sit at the top or bottom of the range?
    tally: dict[str, dict[str, int]] = {}
    for r in rows:
        live = [s for s in r.get("sources", []) if s.get("ok") and s.get("rate")]
        if len(live) < 2:
            continue
        hi = max(live, key=lambda s: s["rate"])["source"]
        lo = min(live, key=lambda s: s["rate"])["source"]
        tally.setdefault(hi, {"highest": 0, "lowest": 0})["highest"] += 1
        tally.setdefault(lo, {"highest": 0, "lowest": 0})["lowest"] += 1

    out: dict = {
        "method": "derived from measured values only",
        "pair": f"{FROM_CCY}/{TO_CCY}",
        "observations": len(rows),
        "observations_with_dispersion": len(disp),
        "first": rows[0]["ts"] if rows else None,
        "last": rows[-1]["ts"] if rows else None,
        "source_extremes": tally,
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    if disp:
        out["dispersion_bps"] = {
            "mean": round(statistics.mean(disp), 3),
            "median": round(statistics.median(disp), 3),
            "min": round(min(disp), 3),
            "max": round(max(disp), 3),
            "stdev": round(statistics.stdev(disp), 3) if len(disp) > 1 else None,
        }
    else:
        out["dispersion_bps"] = None

    # Refuse to imply a finding from too little data.
    n = len(disp)
    out["citable"] = n >= 30
    out["citation_note"] = (
        f"{n} observations. Sufficient to quote a range."
        if n >= 30 else
        f"{n} observations. NOT yet sufficient to cite — needs 30+."
    )
    return out


# ── entry ─────────────────────────────────────────────────────────────

def main() -> int:
    print(f"Lupine spread log · {FROM_CCY}/{TO_CCY}")
    try:
        obs = observe()
    except Exception as e:                       # never break the daily pipeline
        print(f"WARNING: observation failed — {e}")
        return 0

    m = obs["measured"]
    ok = [s for s in obs["sources"] if s["ok"]]
    print(f"  sources reachable : {m['n_sources_ok']}/{m['n_sources_tried']}")
    for s in ok:
        print(f"    {s['source']:<22} {s['rate']:.6f}  ({s['source_date'] or 'no date'})")

    if m.get("dispersion_bps") is not None:
        print(f"  median            : {m['median']:.6f}")
        print(f"  dispersion        : {m['dispersion_bps']} bps  [MEASURED]")
    else:
        print(f"  dispersion        : n/a — {m.get('note','')}")

    print(f"  provider bps      : {len(obs['modelled']['providers'])} entries  [MODELLED — not quotes]")

    append(obs)
    rows = read_log()
    summary = summarise(rows)
    SUM_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\n  log    → {LOG_PATH.name}  ({summary['observations']} observations)")
    print(f"  summary→ {SUM_PATH.name}")
    print(f"  {summary['citation_note']}")
    if summary["dispersion_bps"]:
        d = summary["dispersion_bps"]
        print(f"  dispersion so far : mean {d['mean']} bps · range {d['min']}–{d['max']} bps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
