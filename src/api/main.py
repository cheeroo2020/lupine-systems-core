"""
Lupine Systems V0 — API
Five endpoints matching the V0 spec:
  /create-movement
  /get-routes/{request_id}
  /score-routes/{request_id}
  /execute/{request_id}
  /log/{request_id}
"""
from fastapi import FastAPI, HTTPException
from src.models.schemas import MovementRequest, Urgency
from src.aiva_lite.router import generate_routes
from src.aiva_lite.scorer import score_routes
from src.aiva_lite.selector import select_route
from src.rail_lite.executor import simulate_full_execution
from src.cloked_lite.logger import create_evidence_log, append_evidence, verify_chain

app = FastAPI(
    title="Lupine Systems V0",
    description="Movement decision engine for high-stakes transfers",
    version="0.1.0",
)

# In-memory store (V0 only — no persistence needed)
_store: dict = {}


@app.post("/create-movement")
def create_movement(
    amount: float,
    from_currency: str = "AUD",
    to_currency: str = "SGD",
    urgency: Urgency = Urgency.normal,
):
    """Step 1: Create a movement request."""
    request = MovementRequest(
        amount=amount,
        from_currency=from_currency.upper(),
        to_currency=to_currency.upper(),
        urgency=urgency,
    )

    # Start evidence chain
    evidence = create_evidence_log(request.id)
    evidence = append_evidence(evidence, "request_created", request.model_dump(mode="json"))

    _store[request.id] = {
        "request": request,
        "evidence": evidence,
    }

    return {"request_id": request.id, "status": "created", "request": request}


@app.get("/get-routes/{request_id}")
def get_routes(request_id: str):
    """Step 2: Generate route options."""
    if request_id not in _store:
        raise HTTPException(404, "Request not found")

    request = _store[request_id]["request"]
    routes = generate_routes(request)

    _store[request_id]["routes"] = routes
    _store[request_id]["evidence"] = append_evidence(
        _store[request_id]["evidence"],
        "routes_generated",
        {"routes": [r.model_dump(mode="json") for r in routes]},
    )

    return {"request_id": request_id, "routes": routes}


@app.post("/score-routes/{request_id}")
def score_and_select(request_id: str):
    """Step 3: Score all routes and select the optimal one."""
    if request_id not in _store or "routes" not in _store[request_id]:
        raise HTTPException(404, "Routes not found — call /get-routes first")

    request = _store[request_id]["request"]
    routes = _store[request_id]["routes"]

    scored_routes, weights = score_routes(routes, request.urgency)
    decision = select_route(request.id, scored_routes, weights)

    _store[request_id]["decision"] = decision
    _store[request_id]["evidence"] = append_evidence(
        _store[request_id]["evidence"],
        "routes_scored",
        decision.model_dump(mode="json"),
    )

    return {
        "request_id": request_id,
        "selected": decision.selected_route_name,
        "rationale": decision.rationale,
        "scores": [
            {
                "name": r.name,
                "speed": round(r.speed_score, 3),
                "cost": round(r.cost_score, 3),
                "reliability": round(r.reliability_score, 3),
                "composite": round(r.composite_score, 3),
            }
            for r in scored_routes
        ],
        "weights": weights,
    }


@app.post("/execute/{request_id}")
def execute(request_id: str):
    """Step 4: Simulate execution through the state machine."""
    if request_id not in _store or "decision" not in _store[request_id]:
        raise HTTPException(404, "Decision not found — call /score-routes first")

    decision = _store[request_id]["decision"]
    execution = simulate_full_execution(request_id, decision.selected_route_id)

    _store[request_id]["execution"] = execution
    _store[request_id]["evidence"] = append_evidence(
        _store[request_id]["evidence"],
        "execution_completed",
        execution.model_dump(mode="json"),
    )

    return {
        "request_id": request_id,
        "status": execution.status,
        "route": decision.selected_route_name,
        "state_history": execution.state_history,
    }


@app.get("/log/{request_id}")
def get_log(request_id: str):
    """Step 5: Retrieve the full evidence log."""
    if request_id not in _store:
        raise HTTPException(404, "Request not found")

    evidence = _store[request_id]["evidence"]
    chain_valid = verify_chain(evidence)

    return {
        "request_id": request_id,
        "chain_valid": chain_valid,
        "entries": [
            {
                "seq": e.sequence,
                "event": e.event_type,
                "time": e.timestamp.isoformat(),
                "hash": e.data_hash[:16] + "...",
                "prev": e.previous_hash[:16] + "..." if e.previous_hash != "genesis" else "genesis",
            }
            for e in evidence.entries
        ],
    }


@app.get("/")
def root():
    return {
        "name": "Lupine Systems V0",
        "tagline": "Decide how value moves when it's risky to be wrong",
        "endpoints": [
            "/create-movement",
            "/get-routes/{request_id}",
            "/score-routes/{request_id}",
            "/execute/{request_id}",
            "/log/{request_id}",
        ],
    }
