"""
Aiva-lite Selector — picks the optimal route and generates rationale.
Implements path dominance / Pareto frontier logic from P2-Ch1.
"""
from src.models.schemas import RouteOption, DecisionScore


def select_route(
    request_id: str,
    scored_routes: list[RouteOption],
    weights: dict,
) -> DecisionScore:
    """
    Select the optimal route from scored candidates.
    The route with highest composite_score wins.
    Generate human-readable rationale explaining WHY.
    """
    winner = scored_routes[0]
    runner_up = scored_routes[1] if len(scored_routes) > 1 else None

    # Build rationale
    rationale_parts = [
        f"{winner.name} selected via {winner.corridor}.",
        f"Composite score: {winner.composite_score:.3f}.",
    ]

    if runner_up:
        score_diff = winner.composite_score - runner_up.composite_score
        rationale_parts.append(
            f"Beat {runner_up.name} by {score_diff:.3f} "
            f"({winner.estimated_time_hours}h vs {runner_up.estimated_time_hours}h, "
            f"{winner.estimated_cost_bps}bps vs {runner_up.estimated_cost_bps}bps)."
        )

    # Weight explanation
    dominant_weight = max(weights, key=weights.get)
    rationale_parts.append(
        f"Weights favoured {dominant_weight} "
        f"(speed={weights['speed']:.0%}, cost={weights['cost']:.0%}, "
        f"reliability={weights['reliability']:.0%})."
    )

    return DecisionScore(
        request_id=request_id,
        route_scores=scored_routes,
        selected_route_id=winner.id,
        selected_route_name=winner.name,
        rationale=" ".join(rationale_parts),
        weights_used=weights,
    )
