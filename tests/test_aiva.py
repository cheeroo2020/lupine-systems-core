"""Tests for Aiva-lite: routing, scoring, selection."""
from src.models.schemas import MovementRequest, Urgency
from src.aiva_lite.router import generate_routes
from src.aiva_lite.scorer import score_routes
from src.aiva_lite.selector import select_route


def test_generate_routes_returns_three():
    req = MovementRequest(amount=500000, from_currency="AUD", to_currency="SGD")
    routes = generate_routes(req)
    assert len(routes) == 3


def test_high_urgency_favours_fast_route():
    req = MovementRequest(amount=500000, from_currency="AUD", to_currency="SGD", urgency=Urgency.high)
    routes = generate_routes(req)
    scored, weights = score_routes(routes, req.urgency)
    decision = select_route(req.id, scored, weights)
    assert "Fast" in decision.selected_route_name
    assert weights["speed"] > weights["cost"]


def test_low_urgency_favours_cheap_route():
    req = MovementRequest(amount=500000, from_currency="AUD", to_currency="SGD", urgency=Urgency.low)
    routes = generate_routes(req)
    scored, weights = score_routes(routes, req.urgency)
    decision = select_route(req.id, scored, weights)
    assert weights["cost"] > weights["speed"]


def test_scores_sum_correctly():
    req = MovementRequest(amount=500000, from_currency="AUD", to_currency="SGD")
    routes = generate_routes(req)
    scored, weights = score_routes(routes, req.urgency)
    for r in scored:
        expected = (
            weights["speed"] * r.speed_score
            + weights["cost"] * r.cost_score
            + weights["reliability"] * r.reliability_score
        )
        assert abs(r.composite_score - expected) < 0.001
