"""
Generates website/data/news.json and website/data/health.json from the
latest committed daily-news/ and test-results/ markdown files.

Run by .github/workflows/pages.yml before deploying to GitHub Pages,
and by .github/workflows/daily.yml after daily test+news commits.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR  = REPO_ROOT / "website" / "data"


# ── News parsing ──────────────────────────────────────────────────────

def parse_news_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    stories: list[dict] = []

    # Split on "## " story headings
    parts = re.split(r"\n## ", "\n" + text)
    for part in parts[1:]:
        lines = [l.strip() for l in part.split("\n")]
        headline = lines[0]
        body_lines: list[str] = []
        source = pub_date = ""
        for line in lines[1:]:
            if not line or line == "---":
                continue
            m = re.match(r"\*—\s*(.+?),\s*(.+?)\*$", line)
            if m:
                source   = m.group(1).strip()
                pub_date = m.group(2).strip()
            else:
                body_lines.append(line)
        body = " ".join(body_lines).strip()
        if headline and body:
            stories.append(
                {
                    "headline": headline,
                    "body":     body,
                    "source":   source,
                    "pub_date": pub_date,
                }
            )

    return {"date": path.stem, "stories": stories}


def latest_news() -> dict | None:
    files = sorted(
        (REPO_ROOT / "daily-news").glob("[0-9]*.md"), reverse=True
    )
    for f in files:
        data = parse_news_file(f)
        if data["stories"]:
            return data
    return None


# ── Health parsing ────────────────────────────────────────────────────

def parse_health_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")

    status = "UNKNOWN"
    if "✅ PASSED" in text:
        status = "PASSED"
    elif "❌ FAILED" in text:
        status = "FAILED"

    # Try header first: "**Tests: 14 passed, 0 failed**"
    passed = failed = 0
    m = re.search(r"\*\*Tests:\s*(\d+)\s*passed,\s*(\d+)\s*failed", text)
    if m:
        passed, failed = int(m.group(1)), int(m.group(2))

    # Fallback 1: sum pytest summary lines "===== N passed in 0.10s ====="
    if passed == 0 and failed == 0:
        for mm in re.finditer(r"(\d+)\s+passed\b", text):
            passed += int(mm.group(1))
        for mm in re.finditer(r"(\d+)\s+failed\b", text):
            failed += int(mm.group(1))

    # Fallback 2: markdown table rows "| ✅ PASSED |"
    if passed == 0 and failed == 0:
        passed = text.count("| ✅ PASSED |")
        failed = text.count("| ❌ FAILED |")

    fx_rate = "unavailable"
    for pattern in [
        r"AUD/SGD Rate\s*\|\s*([0-9.]+)",
        r"\|\s*AUD/SGD Rate\s*\|\s*([0-9.]+)",
        r"1 AUD = ([0-9.]+)",
    ]:
        m = re.search(pattern, text)
        if m:
            fx_rate = m.group(1)
            break

    sgd_converted = None
    try:
        rate = float(fx_rate)
        sgd_converted = f"{500_000 * rate:,.0f} SGD"
    except (ValueError, TypeError):
        pass

    return {
        "date":          path.stem,
        "status":        status,
        "passed":        passed,
        "failed":        failed,
        "fx_rate":       fx_rate,
        "sgd_converted": sgd_converted,
    }


def latest_health() -> dict | None:
    files = sorted(
        (REPO_ROOT / "test-results").glob("[0-9]*.md"), reverse=True
    )
    return parse_health_file(files[0]) if files else None


# ── Main ──────────────────────────────────────────────────────────────

def _backtest_is_stale() -> bool:
    """Return True if backtest.json is missing or not generated today.

    Refreshing daily keeps the 14-day "Last trading days" table in sync
    with the calendar. The backtest is cheap (~one Frankfurter call plus
    a few hundred deterministic engine runs) so daily rebuilds are fine.
    """
    p = DATA_DIR / "backtest.json"
    if not p.exists():
        return True
    try:
        generated = json.loads(p.read_text(encoding="utf-8")).get("generated", "")
        return date.fromisoformat(generated) < date.today()
    except Exception:
        return True


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    news = latest_news()
    if news:
        (DATA_DIR / "news.json").write_text(
            json.dumps(news, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"news.json  → {news['date']} ({len(news['stories'])} stories)")
    else:
        print("news.json  → no stories found")

    health = latest_health()
    if health:
        (DATA_DIR / "health.json").write_text(
            json.dumps(health, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"health.json → {health['date']} {health['status']}")
    else:
        print("health.json → no test results found")

    if _backtest_is_stale():
        script = REPO_ROOT / "scripts" / "backtest.py"
        r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        if r.returncode == 0:
            print("backtest.json → regenerated")
        else:
            print(f"backtest.json → FAILED ({r.stderr.strip()[:120]})")
    else:
        print("backtest.json → fresh (skipped)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
