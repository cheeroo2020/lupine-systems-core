"""Tests for the lab's programme and progress files (website/lab/)."""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LAB = ROOT / "website" / "lab"
SESSION_FIELDS = {"id", "day", "title", "study", "concept", "task", "outputs",
                  "equipment", "stop", "checklist", "next"}


def load(name):
    return json.loads((LAB / name).read_text(encoding="utf-8"))


def expand(ref):
    """'01-03..01-06' -> ['01-03', '01-04', '01-05', '01-06']; '01-08' -> ['01-08']."""
    if ".." not in ref:
        return [ref]
    start, end = ref.split("..")
    assert start[:2] == end[:2], f"a range must stay within one part: {ref}"
    return [f"{start[:2]}-{n:02d}" for n in range(int(start[3:]), int(end[3:]) + 1)]


def all_sessions():
    return [s for w in load("programme.json")["weeks"] for s in w["sessions"]]


def test_every_study_reference_is_a_real_textbook_page():
    # Regenerate the index with: python scripts/build_textbook_index.py
    pages = load("textbook-pages.json")["pages"]
    refs = [r for w in load("programme.json")["weeks"]
            for r in w.get("study", []) + [x for s in w["sessions"] for x in s["study"]]]
    for ref in refs:
        assert re.fullmatch(r"0[1-8]-\d\d(\.\.0[1-8]-\d\d)?", ref), ref
        for label in expand(ref):
            assert label in pages, f"{label} is not a page in the course text"


def test_sessions_have_every_field_and_unique_ids():
    sessions = all_sessions()
    assert sessions, "week 1 must be written out in full"
    ids = [s["id"] for s in sessions]
    assert len(ids) == len(set(ids))
    for s in sessions:
        assert SESSION_FIELDS <= set(s), f"{s['id']} is missing {SESSION_FIELDS - set(s)}"
        assert s["outputs"] and all({"what", "saved_to"} <= set(o) for o in s["outputs"])
        assert s["checklist"] and s["stop"]


def test_completed_sessions_exist_and_their_evidence_is_in_the_repository():
    known = {s["id"] for s in all_sessions()}
    for entry in load("progress.json")["sessions"]:
        assert entry["id"] in known
        assert entry["evidence"], f"{entry['id']} is marked complete without evidence"
        for ev in entry["evidence"]:
            path = ROOT / ev["path"]
            assert path.exists(), f"{entry['id']}: evidence {ev['path']} is not in the repository"
            if "contains" in ev:
                assert ev["contains"] in path.read_text(encoding="utf-8"), \
                    f"{entry['id']}: {ev['path']} does not contain {ev['contains']!r}"


def test_writeups_and_firsthand_observations_link_real_evidence():
    progress = load("progress.json")
    targets = load("programme.json")["targets"]
    for w in progress["writeups"]:
        assert w["id"] in targets["writeups"] and (ROOT / w["path"]).exists()
    for obs in progress["observations"]["firsthand"]:
        assert obs.get("synthetic") is not True
        assert (ROOT / obs["path"]).exists(), f"observation {obs['id']} has no record"


def test_demo_data_is_labelled_synthetic_and_never_counts_as_progress():
    demo = load("demo-data.json")
    assert demo["synthetic"] is True
    assert all(run["synthetic"] is True for run in demo["runs"])
    progress = load("progress.json")
    assert demo["session"]["id"].startswith("DEMO-")
    assert demo["session"]["id"] not in {e["id"] for e in progress["sessions"]}
    entries = progress["sessions"] + progress["writeups"] + [o for group in progress["observations"].values() for o in group]
    assert not any(e.get("synthetic") for e in entries)


@pytest.mark.parametrize("ref,expected", [("01-08", ["01-08"]), ("01-03..01-05", ["01-03", "01-04", "01-05"])])
def test_expand(ref, expected):
    assert expand(ref) == expected
