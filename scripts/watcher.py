#!/usr/bin/env python3
"""
Lupine Watcher Agent — autonomous AUD/SGD market monitoring with CLOKED audit.

Runs hourly via GitHub Actions. The agent:
  1. Perceives — fetches live rate + reads recent news files for signals
  2. Reasons  — computes z-score, percentile, momentum from 60-day history
  3. Decides  — emits STRIKE / WATCH / HOLD / NEUTRAL with rationale
  4. Acts     — writes signal JSON, signs CLOKED chain, surfaces strikes via Issues

Goal: catch the top 10% transfer days within a rolling window without manual
monitoring. The CLOKED chain proves what was decided, when, and why.
"""
from __future__ import annotations

import json
import os
import statistics
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.cloked_lite.logger import create_evidence_log, append_evidence, verify_chain

REPO_ROOT     = Path(__file__).resolve().parent.parent
SIGNAL_PATH   = REPO_ROOT / "website" / "data" / "agent_signal.json"
NEWS_DIR      = REPO_ROOT / "daily-news"
HISTORY_DAYS  = 60   # lookback window
RECENT_NEWS   = 3    # how many recent news files to scan

# News keyword classifiers — tuned for AUD→SGD context
SIGNAL_KEYWORDS = {
    "bullish_aud": [
        "rba hike", "rate hike", "rba raises", "aud strengthens",
        "australia inflation", "rba hawkish", "iron ore rally", "commodity surge",
    ],
    "bearish_aud": [
        "rba cut", "rba dovish", "aud weakens", "aud weakness",
        "china slowdown", "commodity drop", "iron ore drop", "australia recession",
    ],
    "sgd_strength": [
        "mas tightening", "mas appreciate", "sgd strong", "singapore hot",
        "singapore inflation", "mas hawkish",
    ],
    "sgd_weakness": [
        "mas neutral", "sgd weakness", "singapore slowdown",
    ],
}


# ── Perception ────────────────────────────────────────────────────────

def fetch_live() -> tuple[float, str]:
    r = requests.get(
        "https://api.frankfurter.app/latest?from=AUD&to=SGD", timeout=10
    )
    r.raise_for_status()
    d = r.json()
    return float(d["rates"]["SGD"]), d["date"]


def fetch_history() -> dict[str, float]:
    end   = date.today()
    start = end - timedelta(days=HISTORY_DAYS + 30)  # buffer for weekends/holidays
    url   = f"https://api.frankfurter.app/{start}..{end}?from=AUD&to=SGD"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    raw = r.json().get("rates", {})
    return {d: v["SGD"] for d, v in sorted(raw.items())}


def read_news_signals() -> list[dict]:
    """Scan recent daily-news files for keyword matches."""
    if not NEWS_DIR.exists():
        return []
    flags: list[dict] = []
    for f in sorted(NEWS_DIR.glob("[0-9]*.md"), reverse=True)[:RECENT_NEWS]:
        text = f.read_text(encoding="utf-8").lower()
        for category, words in SIGNAL_KEYWORDS.items():
            for kw in words:
                if kw in text:
                    flags.append({"category": category, "keyword": kw, "file": f.stem})
    return flags


# ── Reasoning ─────────────────────────────────────────────────────────

def compute_analysis(history: dict[str, float], current: float) -> dict:
    sorted_keys = sorted(history.keys())
    series_60 = [history[k] for k in sorted_keys[-HISTORY_DAYS:]]
    series_30 = [history[k] for k in sorted_keys[-30:]]
    series_7  = [history[k] for k in sorted_keys[-7:]]
    series_3  = [history[k] for k in sorted_keys[-3:]]

    if not series_60:
        return {"error": "no history"}

    mean_60  = statistics.mean(series_60)
    stdev_60 = statistics.stdev(series_60) if len(series_60) > 1 else 0
    mean_30  = statistics.mean(series_30) if series_30 else mean_60

    z_score = (current - mean_60) / stdev_60 if stdev_60 > 0 else 0
    rank    = sum(1 for r in sorted(series_60) if r <= current)
    pct_60  = (rank / len(series_60)) * 100

    momentum_3d = (current - statistics.mean(series_3)) * 10_000 if series_3 else 0  # in pips
    momentum_7d = (current - statistics.mean(series_7)) * 10_000 if series_7 else 0

    return {
        "rate":          round(current, 5),
        "mean_60d":      round(mean_60, 5),
        "mean_30d":      round(mean_30, 5),
        "stdev_60d":     round(stdev_60, 5),
        "z_score":       round(z_score, 2),
        "percentile_60d": round(pct_60, 1),
        "momentum_3d_pips": round(momentum_3d, 1),
        "momentum_7d_pips": round(momentum_7d, 1),
        "history_n":     len(series_60),
    }


def decide(analysis: dict, news_flags: list[dict]) -> tuple[str, str]:
    """Apply rule-based decision logic."""
    if analysis.get("error"):
        return "NEUTRAL", "Insufficient history."

    z   = analysis["z_score"]
    pct = analysis["percentile_60d"]
    m3  = analysis["momentum_3d_pips"]

    bullish_news = any(f["category"] == "bullish_aud" for f in news_flags)
    bearish_news = any(f["category"] == "bearish_aud" for f in news_flags)
    sgd_weak     = any(f["category"] == "sgd_weakness" for f in news_flags)

    # STRIKE — top decile or strong upside with momentum
    if pct >= 90 or z >= 1.5:
        return "STRIKE", f"Top 10% rate over the last {HISTORY_DAYS} days. Act now."
    if z >= 0.8 and m3 > 0:
        return "STRIKE", f"+{z}σ above 60-day mean with positive 3-day momentum. Favourable window."
    if z >= 0.5 and (bullish_news or sgd_weak):
        return "STRIKE", "Above mean with confirming news (bullish AUD or weak SGD)."

    # WATCH — slight upside, hold for stronger signal
    if z >= 0.3 and bullish_news:
        return "WATCH", "Slight upside vs mean; bullish AUD news suggests waiting may pay off."
    if z >= 0.3:
        return "WATCH", "Above mean but not yet in top decile. Hold for confirmation."

    # HOLD — bottom of range or bearish setup
    if pct <= 10 or z <= -1.5:
        return "HOLD", f"Bottom 10% rate over {HISTORY_DAYS} days. Wait for recovery."
    if z <= -0.5 and bearish_news:
        return "HOLD", "Below mean with bearish AUD news. Wait."

    # NEUTRAL — no strong signal
    return "NEUTRAL", "Rate within 1σ of 60-day mean. No actionable edge."


# ── Action ────────────────────────────────────────────────────────────

def emit_signal(signal: dict) -> None:
    SIGNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    SIGNAL_PATH.write_text(json.dumps(signal, indent=2))


def write_github_outputs(signal: str, rate: float, pct: float, rationale: str) -> None:
    """Expose values for downstream workflow steps."""
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        return
    safe_rationale = rationale.replace("\n", " ").replace("'", "’")[:300]
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(f"signal={signal}\n")
        f.write(f"rate={rate}\n")
        f.write(f"percentile={pct}\n")
        f.write(f"rationale={safe_rationale}\n")


# ── Entry ─────────────────────────────────────────────────────────────

def main() -> int:
    print(f"Lupine Watcher · {datetime.utcnow().isoformat()}Z")

    try:
        current, rate_date = fetch_live()
        history            = fetch_history()
    except Exception as e:
        # Frankfurter is intermittently unreachable. The previous signal is
        # still valid for short outages — exit cleanly so the hourly cron
        # doesn't flag every network blip as a workflow failure.
        print(f"WARNING: Frankfurter unreachable — {e}")
        print("Keeping last signal; skipping this run.")
        return 0

    analysis    = compute_analysis(history, current)
    news_flags  = read_news_signals()
    signal, rationale = decide(analysis, news_flags)

    # CLOKED audit chain — every reasoning step is hashed and linked
    request_id = f"watcher-{rate_date}-{datetime.utcnow().strftime('%H%M%S')}"
    evidence   = create_evidence_log(request_id)
    evidence   = append_evidence(evidence, "perception",  {"rate": current, "date": rate_date})
    evidence   = append_evidence(evidence, "analysis",    analysis)
    evidence   = append_evidence(evidence, "news_signals",{"flags": news_flags})
    evidence   = append_evidence(evidence, "decision",    {"signal": signal, "rationale": rationale})

    output = {
        "agent":         "lupine-watcher-v1",
        "generated":     datetime.utcnow().isoformat()[:19] + "Z",
        "rate":          current,
        "rate_date":     rate_date,
        "signal":        signal,
        "rationale":     rationale,
        "analysis":      analysis,
        "news_signals":  news_flags,
        "evidence_hash": evidence.entries[-1].data_hash,
        "chain_valid":   verify_chain(evidence),
        "request_id":    request_id,
    }
    emit_signal(output)
    write_github_outputs(signal, current, analysis.get("percentile_60d", 0), rationale)

    print(f"  Rate: {current} ({rate_date})")
    print(f"  Z-score: {analysis.get('z_score')} · Percentile: {analysis.get('percentile_60d')}%")
    print(f"  News flags: {len(news_flags)}")
    print(f"  → {signal} — {rationale}")
    print(f"  CLOKED: {output['evidence_hash'][:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
