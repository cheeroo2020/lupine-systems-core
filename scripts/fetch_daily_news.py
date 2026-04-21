"""
Fetches live news about cross-border payments, fintech, and FX markets
from Google News RSS and writes a daily digest to daily-news/YYYY-MM-DD.md.

No API key required — uses Google News RSS public feeds.
Run daily by .github/workflows/daily.yml.
"""
from __future__ import annotations

import html
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import requests
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
NEWS_DIR = REPO_ROOT / "daily-news"
README = NEWS_DIR / "README.md"

SEARCHES = [
    "cross-border+payments",
    "international+money+transfer+fintech",
    "SWIFT+payment+rails+correspondent+banking",
    "FX+foreign+exchange+corridor",
]


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def fetch_rss(query: str, max_items: int = 4) -> list[dict]:
    url = (
        f"https://news.google.com/rss/search"
        f"?q={query}&hl=en-US&gl=US&ceid=US:en"
    )
    try:
        resp = requests.get(
            url, timeout=15, headers={"User-Agent": "Mozilla/5.0"}
        )
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        items = []
        for item in root.findall(".//item")[:max_items]:
            title = html.unescape(item.findtext("title", "").strip())
            link = item.findtext("link", "").strip()
            src_el = item.find("source")
            source = src_el.text.strip() if src_el is not None else ""
            pub_date = item.findtext("pubDate", "").strip()
            desc_raw = html.unescape(
                _strip_tags(item.findtext("description", ""))
            )
            # Google News RSS repeats the title in the description — skip it
            if desc_raw.startswith(title[:40]):
                desc_raw = ""
            desc = desc_raw[:280].rsplit(" ", 1)[0] + "…" if len(desc_raw) > 280 else desc_raw
            if title:
                items.append(
                    {
                        "title": title,
                        "link": link,
                        "source": source,
                        "pub_date": pub_date,
                        "description": desc,
                    }
                )
        return items
    except Exception as exc:
        print(f"  warning: could not fetch '{query}': {exc}", file=sys.stderr)
        return []


def deduplicate(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out = []
    for item in items:
        key = item["title"][:70].lower()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def write_digest(today: date, stories: list[dict]) -> Path:
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    path = NEWS_DIR / f"{today.isoformat()}.md"
    pretty = today.strftime("%-d %B %Y")

    lines: list[str] = [
        f"# Daily News — {pretty}",
        "",
        f"*Live financial news relevant to Lupine Systems — cross-border payments, "
        f"fintech, FX, and payment infrastructure — {pretty}*",
        "",
        "---",
        "",
    ]

    if stories:
        for i, s in enumerate(stories, 1):
            lines += [
                f"### {i}. {s['title']}",
                "",
            ]
            if s["description"]:
                lines += [s["description"], ""]
            source_parts = []
            if s["source"]:
                source_parts.append(f"**{s['source']}**")
            if s["pub_date"]:
                source_parts.append(s["pub_date"])
            if source_parts:
                lines.append("  ".join(source_parts))
                lines.append("")
            if s["link"]:
                lines += [f"[Read full article →]({s['link']})", ""]
            lines += ["---", ""]
    else:
        lines += [
            "No stories fetched today — check the workflow log.",
            "",
        ]

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def update_index(today: date, story_count: int) -> None:
    if not README.exists():
        return
    text = README.read_text(encoding="utf-8")
    row = (
        f"| [{today.isoformat()}](./{today.isoformat()}.md)"
        f" | {story_count} stories |\n"
    )
    if today.isoformat() in text:
        return
    text = text.rstrip() + "\n" + row
    README.write_text(text, encoding="utf-8")


def main() -> int:
    today = datetime.now(timezone.utc).date()
    all_items: list[dict] = []
    for q in SEARCHES:
        label = q.replace("+", " ")
        print(f"Fetching: {label}")
        found = fetch_rss(q)
        print(f"  {len(found)} stories")
        all_items.extend(found)

    stories = deduplicate(all_items)[:8]
    path = write_digest(today, stories)
    update_index(today, len(stories))
    print(f"Wrote {len(stories)} stories → {path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
