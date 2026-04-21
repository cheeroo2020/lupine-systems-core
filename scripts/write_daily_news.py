"""
Daily news generator.

Picks today's article from scripts/articles.py based on days since launch
and writes it to daily-news/YYYY-MM-DD.md. Also updates the index table
in daily-news/README.md.

Run daily by .github/workflows/daily.yml — no manual input required.
"""
from __future__ import annotations

import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.articles import ARTICLES, LAUNCH_DATE

NEWS_DIR = REPO_ROOT / "daily-news"
README = NEWS_DIR / "README.md"

INDEX_HEADER = "| Date | Article |\n|------|---------|\n"


def pick_article(today: date) -> tuple[int, dict]:
    days = (today - LAUNCH_DATE).days
    if days < 0:
        days = 0
    index = days % len(ARTICLES)
    return index, ARTICLES[index]


def write_article(today: date, article: dict) -> Path:
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    path = NEWS_DIR / f"{today.isoformat()}.md"
    pretty_date = today.strftime("%-d %B %Y")
    content = (
        f"# {article['title']}\n\n"
        f"**{pretty_date}**\n\n"
        f"{article['body']}\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def update_index(today: date, article: dict) -> None:
    if not README.exists():
        README.write_text(
            "# Daily News — Lupine Systems\n\n"
            "Automatically written each day at 9am UTC.\n\n"
            "## Index\n\n" + INDEX_HEADER,
            encoding="utf-8",
        )

    text = README.read_text(encoding="utf-8")
    row = f"| [{today.isoformat()}](./{today.isoformat()}.md) | {article['title']} |\n"

    if row.strip() in text:
        return

    if "## Index" not in text:
        text = text.rstrip() + "\n\n## Index\n\n" + INDEX_HEADER
    if INDEX_HEADER not in text:
        text = text + "\n" + INDEX_HEADER

    text = text.rstrip() + "\n" + row
    README.write_text(text, encoding="utf-8")


def main() -> int:
    today = datetime.now(timezone.utc).date()
    index, article = pick_article(today)
    path = write_article(today, article)
    update_index(today, article)
    print(f"Wrote article {index + 1}/{len(ARTICLES)}: {article['title']}")
    print(f"  -> {path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
