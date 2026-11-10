"""Tests for the learning site's content (website/content/)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "website" / "content"


def load(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


COV = load("coverage.json")
NEM = COV["outline"]["NEM"]
APR = COV["outline"]["APR"]
LESSONS = {l["id"]: l for m in NEM for l in m["lessons"]}
SECTIONS = {s["id"]: s for c in APR for s in c["sections"]}
CHAPTERS_WITHOUT_SECTIONS = {c["id"] for c in APR if not c["sections"]}
TOPICS = COV["topics"]


def test_the_outline_matches_both_sources():
    # Ten course modules, 85 lessons; the report's executive summary, six chapters, glossary and three appendices.
    assert [m["id"] for m in NEM] == [f"N{i}" for i in range(1, 11)]
    assert len(LESSONS) == 85
    assert [c["id"] for c in APR] == ["AES", "A1", "A2", "A3", "A4", "A5", "A6", "AGL", "AA", "AB", "AC"]
    for m in NEM:
        assert all(m["pdf"][0] <= l["pdf"] <= m["pdf"][1] for l in m["lessons"]), m["id"]
    for c in APR:
        assert all(c["pages"][0] <= s["page"] <= c["pages"][1] for s in c["sections"]), c["id"]


def test_every_lesson_section_and_appendix_is_mapped_to_a_topic():
    # The coverage map's job: catch omissions.
    mapped_nem = {i for t in TOPICS for i in t["nem"]}
    mapped_apr = {i for t in TOPICS for i in t["apr"]}
    assert set(LESSONS) - mapped_nem == set(), "unmapped course lessons"
    assert set(SECTIONS) - mapped_apr == set(), "unmapped report sections"
    assert CHAPTERS_WITHOUT_SECTIONS - mapped_apr == set(), "unmapped report parts"


def test_topics_only_refer_to_real_parts_of_the_sources():
    valid_apr = set(SECTIONS) | {c["id"] for c in APR}
    for t in TOPICS:
        assert set(t["nem"]) <= set(LESSONS), t["id"]
        assert set(t["apr"]) <= valid_apr, t["id"]
        assert t["phase"] in ("foundations", "next")
        assert t["question"].endswith("?") and t["build"]["kind"] and t["build"]["text"]
        for ref in t["key"]:
            assert re.match(r"^(NEM M\d+ L\d+, PDF pp?\. [\d–]+|APR pp?\. [\d–]+)", ref), ref
            for n in re.findall(r"\d+", ref.split("p.", 1)[1].split("(")[0]) if "p." in ref else []:
                assert 1 <= int(n) <= (298 if ref.startswith("NEM") else 127), ref
    assert [t["id"] for t in TOPICS if t["phase"] == "foundations"] == ["F1", "F2", "F3"]


def test_progress_counts_only_chris_own_work_with_dates_and_evidence():
    progress = load("progress.json")
    assert set(progress) == {"note", "read", "built", "explained"}
    topic_ids = {t["id"] for t in TOPICS}
    date = re.compile(r"^2026-\d\d-\d\d$|^20\d\d-\d\d-\d\d$")
    for r in progress["read"]:
        assert r["item"] in LESSONS or r["item"] in SECTIONS or r["item"] in {c["id"] for c in APR}
        assert date.match(r["date"])
    for kind in ("built", "explained"):
        for e in progress[kind]:
            assert e["topic"] in topic_ids and date.match(e["date"]) and e["evidence"].strip()


def test_portfolio_items_say_what_they_cannot_tell_us():
    for item in load("portfolio.json"):
        for field in ("title", "question", "sources", "mine", "cannot_tell", "date", "topic"):
            assert item.get(field), (item.get("title"), field)


def test_the_sources_are_never_published_on_the_site():
    assert not list((ROOT / "website").rglob("*.pdf"))
