"""
Lupine Systems V0 — API
Five endpoints matching the V0 spec:
  /create-movement
  /get-routes
  /score-routes
  /execute
  /log

Plus /recommend — one-shot pipeline with live FX (used by the website demo).
"""
import json
import os
from pathlib import Path
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

# Browser-callable from the GitHub Pages site (and anywhere else).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
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


class RecommendRequest(BaseModel):
    amount: float = 500000
    from_currency: str = "AUD"
    to_currency: str = "SGD"
    urgency: Urgency = Urgency.normal


@app.post("/recommend")
def recommend(req: RecommendRequest):
    """One-shot pipeline: live FX → routes → scoring → selection → evidence hash.

    Returns everything the website demo needs in a single call.
    """
    request = MovementRequest(
        amount=req.amount,
        from_currency=req.from_currency.upper(),
        to_currency=req.to_currency.upper(),
        urgency=req.urgency,
    )

    fx_rate, fx_date = None, None
    try:
        r = requests.get(
            f"https://api.frankfurter.app/latest?from={request.from_currency}&to={request.to_currency}",
            timeout=5,
        )
        if r.ok:
            d = r.json()
            fx_rate = d.get("rates", {}).get(request.to_currency)
            fx_date = d.get("date")
    except Exception:
        pass

    routes = generate_routes(request, fx_rate=fx_rate)
    scored_routes, weights = score_routes(routes, request.urgency)
    decision = select_route(request.id, scored_routes, weights)

    evidence = create_evidence_log(request.id)
    evidence = append_evidence(evidence, "request_created", request.model_dump(mode="json"))
    evidence = append_evidence(evidence, "fx_observed", {"rate": fx_rate, "date": fx_date})
    evidence = append_evidence(evidence, "routes_scored", decision.model_dump(mode="json"))

    final_hash = evidence.entries[-1].data_hash
    selected = next((r for r in scored_routes if r.id == decision.selected_route_id), scored_routes[0])

    return {
        "request_id": request.id,
        "amount": req.amount,
        "from": request.from_currency,
        "to": request.to_currency,
        "urgency": request.urgency,
        "fx": {
            "rate": fx_rate,
            "date": fx_date,
            "converted": round(req.amount * fx_rate, 2) if fx_rate else None,
            "source": "frankfurter.app (ECB)",
        },
        "selected": {
            "name": selected.name,
            "corridor": selected.corridor,
            "time_hours": selected.estimated_time_hours,
            "cost_bps": selected.estimated_cost_bps,
            "reliability": selected.reliability_score,
            "composite_score": round(selected.composite_score, 3),
        },
        "rationale": decision.rationale,
        "weights": weights,
        "all_routes": [
            {
                "name": r.name,
                "speed": round(r.speed_score, 3),
                "cost": round(r.cost_score, 3),
                "reliability": round(r.reliability_score, 3),
                "composite": round(r.composite_score, 3),
            }
            for r in scored_routes
        ],
        "evidence_hash": final_hash,
        "chain_valid": verify_chain(evidence),
    }


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


# ── Conversational Analyst (Tier 2 agent) ─────────────────────────────

class ChatMessage(BaseModel):
    role: str           # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


def _tool_get_live_rate() -> dict:
    try:
        r = requests.get("https://api.frankfurter.app/latest?from=AUD&to=SGD", timeout=8)
        d = r.json()
        return {"rate": d["rates"]["SGD"], "date": d["date"], "source": "ECB via Frankfurter"}
    except Exception as e:
        return {"error": str(e)}


def _tool_get_recommendation(amount: float, urgency: str) -> dict:
    """Run the full pipeline; return a compact decision summary."""
    fx = _tool_get_live_rate()
    rate = fx.get("rate")
    if rate is None:
        return {"error": "Could not fetch live rate"}

    request = MovementRequest(
        amount=amount, from_currency="AUD", to_currency="SGD",
        urgency=Urgency(urgency),
    )
    routes          = generate_routes(request, fx_rate=rate)
    scored, weights = score_routes(routes, request.urgency)
    decision        = select_route(request.id, scored, weights)
    winner          = next(r for r in scored if r.id == decision.selected_route_id)
    bank            = next((r for r in scored if r.name == "Bank SWIFT"), scored[-1])
    saving          = round(amount * (bank.estimated_cost_bps - winner.estimated_cost_bps) / 10_000, 2)

    evidence = create_evidence_log(request.id)
    evidence = append_evidence(evidence, "request_created", request.model_dump(mode="json"))
    evidence = append_evidence(evidence, "fx_observed",     {"rate": rate})
    evidence = append_evidence(evidence, "routes_scored",   decision.model_dump(mode="json"))

    return {
        "winner":        winner.name,
        "fee_bps":       winner.estimated_cost_bps,
        "settlement_h":  winner.estimated_time_hours,
        "composite":     round(winner.composite_score, 3),
        "saving_vs_bank_aud": saving,
        "weights":       weights,
        "rationale":     decision.rationale,
        "evidence_hash": evidence.entries[-1].data_hash[:32],
        "fx_rate":       rate,
    }


def _tool_get_watcher_signal() -> dict:
    p = Path(__file__).resolve().parent.parent.parent / "website" / "data" / "agent_signal.json"
    if not p.exists():
        return {"error": "no signal file"}
    return json.loads(p.read_text(encoding="utf-8"))


def _tool_get_backtest() -> dict:
    p = Path(__file__).resolve().parent.parent.parent / "website" / "data" / "backtest.json"
    if not p.exists():
        return {"error": "no backtest"}
    full = json.loads(p.read_text(encoding="utf-8"))
    return {
        "n_days":     full.get("n_days"),
        "rate_range": full.get("rate_range"),
        "summary":    full.get("summary"),
    }


CHAT_TOOLS = [
    {
        "name": "get_live_rate",
        "description": "Get the current AUD/SGD mid-market rate from the ECB (via Frankfurter).",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_recommendation",
        "description": "Run the full Lupine decision engine for a given AUD amount and urgency. Returns the winning provider, fee, savings vs bank, and a CLOKED evidence hash.",
        "input_schema": {
            "type": "object",
            "properties": {
                "amount":  {"type": "number", "description": "Amount in AUD"},
                "urgency": {"type": "string", "enum": ["low", "normal", "high", "critical"]},
            },
            "required": ["amount", "urgency"],
        },
    },
    {
        "name": "get_watcher_signal",
        "description": "Get the autonomous Lupine Watcher agent's latest market signal (STRIKE/WATCH/HOLD/NEUTRAL) with reasoning.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_backtest",
        "description": "Get summary of the 90-day backtest: typical savings vs bank for each urgency level.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
]


def _dispatch_tool(name: str, args: dict) -> dict:
    if name == "get_live_rate":      return _tool_get_live_rate()
    if name == "get_recommendation": return _tool_get_recommendation(**args)
    if name == "get_watcher_signal": return _tool_get_watcher_signal()
    if name == "get_backtest":       return _tool_get_backtest()
    return {"error": f"unknown tool {name}"}


SYSTEM_PROMPT = """You are the Lupine analyst — a financial concierge for AUD→SGD cross-border transfers.

You have tools to query the live engine. Always call tools to ground your answers in real data — never fabricate rates, savings figures, or evidence hashes.

Your style: concise, direct, treasury-grade. No hype, no emoji unless mirroring user. Cite numbers with units. When you give a recommendation, briefly explain *why* (which weight dominated, what the percentile means). If you give an evidence hash, frame it as a verifiable record the user can cite.

If the user asks vague things like "should I transfer today?" use get_live_rate + get_watcher_signal first, then suggest a concrete urgency level."""


@app.post("/chat")
def chat(req: ChatRequest):
    """Conversational analyst — Claude with tool access to the Lupine engine.
    Requires ANTHROPIC_API_KEY env var on the deployed instance.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(503, "Chat endpoint requires ANTHROPIC_API_KEY env var")

    try:
        from anthropic import Anthropic
    except ImportError:
        raise HTTPException(500, "anthropic package not installed")

    client = Anthropic(api_key=api_key)

    messages = [{"role": m.role, "content": m.content} for m in req.history]
    messages.append({"role": "user", "content": req.message})

    tool_calls_made: list[dict] = []
    final_text = ""
    max_iterations = 6   # cap recursive tool use

    for _ in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=CHAT_TOOLS,
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            assistant_blocks = []
            tool_results = []
            for block in response.content:
                if block.type == "text":
                    assistant_blocks.append({"type": "text", "text": block.text})
                elif block.type == "tool_use":
                    assistant_blocks.append({
                        "type": "tool_use", "id": block.id,
                        "name": block.name, "input": block.input,
                    })
                    result = _dispatch_tool(block.name, block.input or {})
                    tool_calls_made.append({"tool": block.name, "input": block.input, "result": result})
                    tool_results.append({
                        "type": "tool_result", "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })
            messages.append({"role": "assistant", "content": assistant_blocks})
            messages.append({"role": "user",      "content": tool_results})
            continue

        # stop_reason == "end_turn"
        for block in response.content:
            if block.type == "text":
                final_text += block.text
        break

    return {
        "response":    final_text or "(no response)",
        "tool_calls":  tool_calls_made,
        "model":       "claude-sonnet-4-6",
    }


@app.get("/")
def root():
    return {
        "name": "Lupine Systems V0",
        "tagline": "Decide how value moves when it's risky to be wrong",
        "endpoints": [
            "/recommend",
            "/chat",
            "/create-movement",
            "/get-routes/{request_id}",
            "/score-routes/{request_id}",
            "/execute/{request_id}",
            "/log/{request_id}",
            "/healthz",
            "/docs",
        ],
    }
