"""
Fetches live financial news relevant to Lupine Systems (cross-border
payments, fintech, FX, payment infrastructure) from payments-focused
RSS feeds that include real article summaries.

Writes a digest to daily-news/YYYY-MM-DD.md with 2 summarised stories
and their sources. No API key required.

Run daily by .github/workflows/daily.yml.
"""
from __future__ import annotations

import html
import re
import sys
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
NEWS_DIR = REPO_ROOT / "daily-news"
README = NEWS_DIR / "README.md"

SOURCES = [
    ("PYMNTS", "https://www.pymnts.com/feed/"),
    ("American Banker", "https://www.americanbanker.com/feed?rss=true"),
]

RELEVANCE_KEYWORDS = [
    "cross-border", "cross border", "payment", "payments", "remittance",
    "transfer", "fx", "foreign exchange", "currency", "fintech",
    "swift", "correspondent", "corridor", "stablecoin", "settlement",
    "clearing", "real-time payment", "rtp", "interbank", "wire",
    "bank", "visa", "mastercard", "ripple", "treasury",
]


def _clean(text: str, limit: int | None = None) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    # Pymnts appends "The post X appeared first on …" — trim it
    text = re.sub(r"\s*The post .*?appeared first on.*$", "", text)
    if limit and len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text


def _is_relevant(title: str, description: str) -> bool:
    blob = (title + " " + description).lower()
    return any(k in blob for k in RELEVANCE_KEYWORDS)


def _parse_date(s: str):
    try:
        return parsedate_to_datetime(s)
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)


def fetch_source(name: str, url: str) -> list[dict]:
    try:
        resp = requests.get(
            url, timeout=15, headers={"User-Agent": "Mozilla/5.0"}
        )
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
    except Exception as exc:
        print(f"  warning: {name}: {exc}", file=sys.stderr)
        return []

    items = []
    for item in root.findall(".//item"):
        title = _clean(item.findtext("title", ""))
        description = _clean(item.findtext("description", ""), limit=600)
        link = item.findtext("link", "").strip()
        pub_date = item.findtext("pubDate", "").strip()
        if not (title and description):
            continue
        if not _is_relevant(title, description):
            continue
        items.append(
            {
                "title": title,
                "description": description,
                "link": link,
                "source": name,
                "pub_date": pub_date,
                "sort_key": _parse_date(pub_date),
            }
        )
    return items


def pick_stories(all_items: list[dict], n: int = 2) -> list[dict]:
    seen_sources: set[str] = set()
    sorted_items = sorted(all_items, key=lambda x: x["sort_key"], reverse=True)
    picked: list[dict] = []
    # Prefer one story per source first
    for item in sorted_items:
        if len(picked) >= n:
            break
        if item["source"] not in seen_sources:
            picked.append(item)
            seen_sources.add(item["source"])
    # Fill with most recent if still short
    for item in sorted_items:
        if len(picked) >= n:
            break
        if item not in picked:
            picked.append(item)
    return picked


def format_pub_date(raw: str) -> str:
    try:
        dt = parsedate_to_datetime(raw)
        return dt.strftime("%d %b %Y")
    except Exception:
        return raw or ""


def write_digest(today: date, stories: list[dict]) -> Path:
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    path = NEWS_DIR / f"{today.isoformat()}.md"
    pretty = today.strftime("%-d %B %Y")

    lines: list[str] = [
        f"# Daily News — {pretty}",
        "",
        "*Live headlines on cross-border payments, fintech, and FX — "
        "fetched from PYMNTS and American Banker.*",
        "",
        "---",
        "",
    ]

    if not stories:
        lines += [
            "No relevant stories found today. Check workflow logs.",
            "",
        ]
    else:
        for s in stories:
            lines += [
                f"## {s['title']}",
                "",
                s["description"],
                "",
                f"*— {s['source']}, {format_pub_date(s['pub_date'])}*",
                "",
                "---",
                "",
            ]

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def update_index(today: date, stories: list[dict]) -> None:
    if not README.exists():
        return
    text = README.read_text(encoding="utf-8")
    if today.isoformat() in text:
        return
    headline = stories[0]["title"] if stories else "—"
    if len(headline) > 70:
        headline = headline[:67] + "…"
    row = f"| [{today.isoformat()}](./{today.isoformat()}.md) | {headline} |\n"
    text = text.rstrip() + "\n" + row
    README.write_text(text, encoding="utf-8")


def main() -> int:
    today = datetime.now(timezone.utc).date()
    all_items: list[dict] = []
    for name, url in SOURCES:
        print(f"Fetching: {name}")
        items = fetch_source(name, url)
        print(f"  {len(items)} relevant items")
        all_items.extend(items)

    stories = pick_stories(all_items, n=2)
    path = write_digest(today, stories)
    update_index(today, stories)
    print(f"Wrote {len(stories)} stories → {path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
