"""
Live integration tests — pull real-time AUD/SGD FX rate from Frankfurter API
and run the full V0 pipeline against actual market data.

These run daily via GitHub Actions. Results are written to test-results/.
"""
import pytest
import requests
from src.data.fx_feed import fetch_fx_rate
from src.models.schemas import MovementRequest, Urgency
from src.aiva_lite.router import generate_routes
from src.aiva_lite.scorer import score_routes
from src.aiva_lite.selector import select_route
from src.rail_lite.executor import simulate_full_execution
from src.cloked_lite.logger import create_evidence_log, append_evidence, verify_chain


def test_frankfurter_api_reachable():
    """Confirm the FX data source is online and returning valid data."""
    fx = fetch_fx_rate("AUD", "SGD")
    assert "rate" in fx
    assert "date" in fx
    assert isinstance(fx["rate"], float)
    assert fx["rate"] > 0
    print(f"\nFrankfurter API: 1 AUD = {fx['rate']} SGD (as of {fx['date']})")


def test_live_aud_sgd_high_urgency():
    """Full pipeline using live rate — high urgency (speed-favoured)."""
    fx = fetch_fx_rate("AUD", "SGD")
    amount_aud = 500_000
    amount_sgd = round(amount_aud * fx["rate"], 2)

    req = MovementRequest(
        amount=amount_aud,
        from_currency="AUD",
        to_currency="SGD",
        urgency=Urgency.high,
    )
    routes = generate_routes(req)
    scored, weights = score_routes(routes, req.urgency)
    decision = select_route(req.id, scored, weights)
    execution = simulate_full_execution(req.id, decision.selected_route_id)

    assert execution.status.value == "completed"
    print(f"\n[high urgency] 1 AUD = {fx['rate']} SGD | 500,000 AUD = {amount_sgd:,.2f} SGD")
    print(f"Selected: {decision.selected_route_name} | Score: {scored[0].composite_score:.3f}")
    print(f"Rationale: {decision.rationale}")


def test_live_aud_sgd_low_urgency():
    """Full pipeline using live rate — low urgency (cost-favoured)."""
    fx = fetch_fx_rate("AUD", "SGD")
    amount_aud = 500_000

    req = MovementRequest(
        amount=amount_aud,
        from_currency="AUD",
        to_currency="SGD",
        urgency=Urgency.low,
    )
    routes = generate_routes(req)
    scored, weights = score_routes(routes, req.urgency)
    decision = select_route(req.id, scored, weights)
    execution = simulate_full_execution(req.id, decision.selected_route_id)

    assert execution.status.value == "completed"
    assert weights["cost"] > weights["speed"]
    print(f"\n[low urgency] Selected: {decision.selected_route_name} | Score: {scored[0].composite_score:.3f}")


def test_live_evidence_chain_with_real_rate():
    """Evidence chain integrity using a live FX rate embedded in the payload."""
    fx = fetch_fx_rate("AUD", "SGD")

    log = create_evidence_log("live-test")
    log = append_evidence(log, "live_fx_snapshot", {
        "source": "frankfurter.app",
        "from": fx["from"],
        "to": fx["to"],
        "rate": fx["rate"],
        "date": fx["date"],
    })
    log = append_evidence(log, "movement_created", {
        "amount_aud": 500_000,
        "amount_sgd": round(500_000 * fx["rate"], 2),
    })

    assert verify_chain(log) is True
    print(f"\nEvidence chain valid. Rate embedded: 1 AUD = {fx['rate']} SGD")
