"""Tests for Grid Desk's data file (website/desk/data/apr-2026.json)."""
import json
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parent.parent / "website" / "desk" / "data" / "apr-2026.json").read_text(encoding="utf-8"))
ROWS = DATA["table_4_1"]["rows"]


def test_table_4_1_has_every_substation_by_area():
    # Counted from the report's Table 4-1 (printed pp. 62-63).
    counts = {}
    for r in ROWS:
        counts[r["area"]] = counts.get(r["area"], 0) + 1
    assert counts == {"North West and West Coast": 17, "Northern": 11, "Central": 6, "Southern": 28}
    assert len({(r["area"], r["name"]) for r in ROWS}) == len(ROWS)


def test_headroom_matches_firm_capacity_minus_demand():
    # The report's own arithmetic: firm headroom = firm capacity - 2026 maximum demand, never below
    # zero, rounded. Rows flagged with a sub-transmission constraint may be lower. A transcription
    # error in any row breaks this.
    for r in ROWS:
        demand = r["max_demand_2026_mva"] if r["max_demand_2026_mva"] is not None else 0
        expected = max(0.0, r["installed_firm_mva"] - demand)
        if "subtransmission_constraint" in r["flags"]:
            assert r["firm_headroom_mva"] <= expected + 0.5, r["name"]
        else:
            assert abs(r["firm_headroom_mva"] - expected) <= 0.5, (r["name"], r["firm_headroom_mva"], expected)
        assert r["installed_firm_mva"] <= r["installed_total_mva"], r["name"]


def test_every_figure_has_a_page_in_the_report():
    pages = [r["page"] for r in ROWS]
    for section in (DATA["rules"], DATA["context"], DATA["system_strength_nodes"]["outlook"]):
        for item in section.values():
            pages += item["pages"]
    pages += DATA["definitions"]["firm"]["pages"]
    assert all(isinstance(p, int) and 1 <= p <= 127 for p in pages)


def test_every_planning_area_maps_to_a_system_strength_node():
    nodes = DATA["system_strength_nodes"]
    areas = {r["area"] for r in ROWS}
    assert areas == set(nodes["area_to_node"])
    assert set(nodes["area_to_node"].values()) == set(nodes["outlook"])
