"""
Aiva-lite Scorer — multi-dimension scoring engine.
Implements the composite utility function from the book:
U(R) = w1*Speed + w2*Cost + w3*Reliability

Weights shift based on urgency (from Ch P2-2).
"""
from src.models.schemas import RouteOption, Urgency


# Weight profiles based on urgency
WEIGHT_PROFILES = {
    Urgency.low:      {"speed": 0.15, "cost": 0.55, "reliability": 0.30},
    Urgency.normal:   {"speed": 0.25, "cost": 0.35, "reliability": 0.40},
    Urgency.high:     {"speed": 0.50, "cost": 0.15, "reliability": 0.35},
    Urgency.critical: {"speed": 0.60, "cost": 0.05, "reliability": 0.35},
}


def score_routes(routes: list[RouteOption], urgency: Urgency) -> tuple[list[RouteOption], dict]:
    """
    Score all routes using the composite utility function.
    Returns scored routes and the weights used.

    Speed score: inverse of time (faster = higher)
    Cost score: inverse of cost (cheaper = higher)
    Reliability score: direct (higher = better)

    All normalised to 0-1 range before weighting.
    """
    weights = WEIGHT_PROFILES[urgency]

    # Find ranges for normalisation
    max_time = max(r.estimated_time_hours for r in routes)
    max_cost = max(r.estimated_cost_bps for r in routes)

    for route in routes:
        # Compute individual scores (normalised 0-1, higher = better)
        route.speed_score = 1.0 - (route.estimated_time_hours / max_time)
        route.cost_score = 1.0 - (route.estimated_cost_bps / max_cost)
        # reliability_score is already 0-1

        # Composite utility
        route.composite_score = (
            weights["speed"] * route.speed_score
            + weights["cost"] * route.cost_score
            + weights["reliability"] * route.reliability_score
        )

    # Sort by composite score descending
    routes.sort(key=lambda r: r.composite_score, reverse=True)

    return routes, weights
