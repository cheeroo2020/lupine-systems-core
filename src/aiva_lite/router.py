"""
Aiva-lite Router — generates candidate route options.
In V0, routes are simulated (not from live data).
"""
from src.models.schemas import MovementRequest, RouteOption


def generate_routes(request: MovementRequest) -> list[RouteOption]:
    """
    Generate candidate routes for a movement request.
    V0: returns 3 simulated routes (Fast, Cheap, Balanced).
    Future: pulls from live corridor data, liquidity graphs, etc.
    """
    routes = [
        RouteOption(
            name="Fast Route",
            corridor=f"{request.from_currency} → {request.to_currency} direct (Tier 1)",
            estimated_time_hours=2.5,
            estimated_cost_bps=45.0,
            reliability_score=0.82,
        ),
        RouteOption(
            name="Cheap Route",
            corridor=f"{request.from_currency} → USD → {request.to_currency} (regional pool)",
            estimated_time_hours=18.0,
            estimated_cost_bps=12.0,
            reliability_score=0.71,
        ),
        RouteOption(
            name="Balanced Route",
            corridor=f"{request.from_currency} → {request.to_currency} (Tier 2 regional)",
            estimated_time_hours=6.0,
            estimated_cost_bps=28.0,
            reliability_score=0.93,
        ),
    ]
    return routes
