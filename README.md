# LUPINE SYSTEMS — README

## Overview
Lupine Systems is a multi-layer value‑movement architecture composed of three coordinated subsystems:

- **AIVA** — Intelligent multi‑graph routing & risk evaluation  
- **LUPINE RAIL** — Resilient settlement & movement pipeline  
- **CLOKED** — Evidence, audit & verifiable truth layer  

This README summarises Phase 1 development progress, includes architecture diagrams, and documents the implemented components.

---

## 🌐 High‑Level Architecture

```mermaid
flowchart TD
    AIVA[AIVA Intelligence Layer] --> RAIL[Lupine Rail Execution Layer]
    RAIL --> CLOKED[Cloked Evidence Layer]

    subgraph AIVA Intelligence
        MG[Medical Graph]
        VG[Volatility Graph]
        CG[Compliance Graph]
        LG[Liquidity Graph]
        HG[Hop Graph]
        MERGE[Multi-Graph Merge Engine]
        MG --> MERGE
        VG --> MERGE
        CG --> MERGE
        LG --> MERGE
        HG --> MERGE
    end

    subgraph RAIL Execution
        SM[State Machine]
        EX[Rail Executor]
        EV[Structured Event Log]
        SM --> EX
        EX --> EV
    end

    subgraph CLOKED Evidence
        AUD[Hash-linked Evidence Capsule]
    end

    EV --> AUD
```

---

## 🚀 AIVA: Intelligence Layer

AIVA decides whether a route is safe, viable, liquid, and compliant using five graph engines:

### 🫀 MedicalGraph (Thermal Viability)
- Determines biological viability based on:
  - payload type  
  - transit duration  
  - container temperature  
- Implements deterministic spoilage thresholds.

### 📉 VolatilityGraph (FX Market Conditions)
- Normalises FX volatility into a safety score.  
- Rejects if above configured threshold.

### 🛂 ComplianceGraph (Sanctions Risk)
- Rejects blacklisted countries.  
- Flags high-risk corridors.

### 💧 LiquidityGraph (Funding Capacity)
- Simulates available balances per node.  
- Rejects insufficient liquidity.

### 🔗 HopGraph & Merge Engine
- Builds settlement corridors.  
- Merges risk + liquidity + volatility + compliance into a unified score.

---

## 🚂 LUPINE RAIL: Execution Layer

### 🔧 Transaction State Machine

```mermaid
stateDiagram-v2
    [*] --> CREATED
    CREATED --> AIVA_CHECKING
    AIVA_CHECKING --> AIVA_REJECTED
    AIVA_CHECKING --> LIQUIDITY_LOCKED
    LIQUIDITY_LOCKED --> IN_FLIGHT
    IN_FLIGHT --> FAILED
    IN_FLIGHT --> SETTLED
```

### 🛠 Rail Executor
- Performs settlement hops.  
- Includes **Chaos Monkey (25% chance of network failure)**.  
- Implements **Retry Logic (max 3 attempts per hop)**.

### 🧾 Structured Event Logging (Story 4.4)
Every hop, attempt, retry, success, and final settlement is captured as a structured event:

- UUID  
- Timestamp  
- Event Type  
- Details (node, attempt, status, etc.)

---

## 🔐 CLOKED: Evidence Layer

Hash‑linked audit log ensuring immutability and forensic replayability:

- Every event hashed  
- Linked to previous event  
- Replayable chain (like a mini blockchain)

---

## 🧪 Test Suite (tests/test_risk_scenarios.py)

The system includes six scenarios:

1. **Scenario A** — Medical Fast Route  
2. **Scenario B** — Medical Slow Route  
3. **Scenario C** — FX Market Crash  
4. **Scenario D** — Sanctions Compliance Failure  
5. **Scenario E** — Liquidity Crunch  
6. **Scenario F** — Rail Resilience (Retries & Failover)

---

## 📦 Project Structure

```
lupine-systems-core/
├── src/
│   ├── models/                   # V0 Pydantic data models
│   │   └── schemas.py
│   ├── aiva_lite/                # V0 Intelligence layer
│   │   ├── router.py             #   route generation
│   │   ├── scorer.py             #   composite utility scoring
│   │   └── selector.py           #   winner selection + rationale
│   ├── rail_lite/                # V0 Execution layer
│   │   └── executor.py           #   state machine
│   ├── cloked_lite/              # V0 Evidence layer
│   │   └── logger.py             #   SHA-256 hash chain
│   ├── api/                      # V0 FastAPI app
│   │   └── main.py               #   5 endpoints
│   ├── aiva/                     # Phase 1 — full graph engines
│   │   ├── medical_graph.py
│   │   ├── volatility_graph.py
│   │   ├── compliance_graph.py
│   │   ├── liquidity_graph.py
│   │   ├── hop_graph.py
│   │   └── merge_engine.py
│   ├── rail/                     # Phase 1 — full executor
│   │   ├── state_machine.py
│   │   ├── executor.py
│   │   └── events.py
│   └── cloked/                   # Phase 1 — full auditor
│       └── auditor.py
├── tests/
│   ├── test_aiva.py              # V0 routing + scoring tests
│   ├── test_rail.py              # V0 state machine tests
│   ├── test_cloked.py            # V0 evidence chain tests
│   └── test_risk_scenarios.py    # Phase 1 risk scenarios
├── docs/
│   └── v0_spec.md
└── main_skeleton.py
```

---

## V0 — Movement Decision Engine

> V0 is the first working loop: take a request, score routes, pick the best, simulate execution, produce proof.

### V0 System Overview

```mermaid
flowchart LR
    User -->|POST /create-movement| API

    subgraph API["FastAPI — src/api/main.py"]
        EP1["/create-movement"]
        EP2["/get-routes"]
        EP3["/score-routes"]
        EP4["/execute"]
        EP5["/log"]
    end

    subgraph AIVA_LITE["Aiva-lite — Intelligence"]
        R[router.py\nGenerate 3 routes]
        S[scorer.py\nComposite utility score]
        SEL[selector.py\nPick winner + rationale]
        R --> S --> SEL
    end

    subgraph RAIL_LITE["Rail-lite — Execution"]
        SM2[executor.py\nState machine]
    end

    subgraph CLOKED_LITE["Cloked-lite — Evidence"]
        L[logger.py\nSHA-256 hash chain]
    end

    EP2 --> R
    EP3 --> S
    EP3 --> SEL
    EP4 --> SM2
    EP1 & EP2 & EP3 & EP4 --> L
    EP5 --> L
```

---

### V0 API — 5-Step Flow

```mermaid
sequenceDiagram
    actor User
    participant API
    participant Aiva-lite
    participant Rail-lite
    participant Cloked-lite

    User->>API: POST /create-movement\n(amount, from, to, urgency)
    API->>Cloked-lite: log "request_created"
    API-->>User: request_id

    User->>API: GET /get-routes/{request_id}
    API->>Aiva-lite: generate_routes()
    Aiva-lite-->>API: [Fast, Cheap, Balanced]
    API->>Cloked-lite: log "routes_generated"
    API-->>User: 3 route options

    User->>API: POST /score-routes/{request_id}
    API->>Aiva-lite: score_routes() → select_route()
    Aiva-lite-->>API: winner + rationale
    API->>Cloked-lite: log "routes_scored"
    API-->>User: selected route + scores

    User->>API: POST /execute/{request_id}
    API->>Rail-lite: simulate_full_execution()
    Rail-lite-->>API: completed state
    API->>Cloked-lite: log "execution_completed"
    API-->>User: status + state history

    User->>API: GET /log/{request_id}
    API->>Cloked-lite: verify_chain()
    Cloked-lite-->>API: entries + chain_valid
    API-->>User: full evidence log
```

---

### Aiva-lite — Route Scoring

Composite utility: **U = w₁·Speed + w₂·Cost + w₃·Reliability**

Weights shift automatically based on urgency:

| Urgency  | Speed | Cost | Reliability |
|----------|------:|-----:|------------:|
| low      |  15%  |  55% |         30% |
| normal   |  25%  |  35% |         40% |
| high     |  50%  |  15% |         35% |
| critical |  60%  |   5% |         35% |

```mermaid
flowchart TD
    REQ[Movement Request\nurgency: high] --> WP[Weight Profile\nspeed=50% cost=15% reliability=35%]
    WP --> NORM[Normalise scores 0→1\nspeed: 1 - time/max_time\ncost:  1 - cost/max_cost]

    NORM --> R1["Fast Route\nspeed=1.0 cost=0.27 rel=0.82\nU = 0.50×1.0 + 0.15×0.27 + 0.35×0.82 = 0.829"]
    NORM --> R2["Cheap Route\nspeed=0.0 cost=1.0 rel=0.71\nU = 0.50×0.0 + 0.15×1.0 + 0.35×0.71 = 0.399"]
    NORM --> R3["Balanced Route\nspeed=0.86 cost=0.62 rel=0.93\nU = 0.50×0.86 + 0.15×0.62 + 0.35×0.93 = 0.849"]

    R1 & R2 & R3 --> WIN["Winner: Balanced Route\nscore 0.849"]

    style WIN fill:#22c55e,color:#fff
```

---

### Rail-lite — Execution State Machine

```mermaid
stateDiagram-v2
    direction LR
    [*] --> initiated
    initiated --> scored
    scored --> route_selected
    route_selected --> executing
    executing --> completed
    executing --> failed
    completed --> [*]
    failed --> [*]
```

Invalid transitions raise `ValueError` — the state machine enforces every step.

---

### Cloked-lite — SHA-256 Evidence Chain

```mermaid
flowchart LR
    G([genesis]) --> E0

    E0["Entry 0\nevent: request_created\nhash: a3f9..."]
    E1["Entry 1\nevent: routes_generated\nhash: 7c2b..."]
    E2["Entry 2\nevent: routes_scored\nhash: 1e4d..."]
    E3["Entry 3\nevent: execution_completed\nhash: 9f8a..."]

    E0 -->|prev_hash| E1
    E1 -->|prev_hash| E2
    E2 -->|prev_hash| E3

    NOTE["verify_chain() recomputes\nevery hash and checks linkage.\nAny tamper = False."]
```

---

## 📈 Progress

### V0 — Movement Decision Engine

| Component | Status | Details |
|-----------|--------|---------|
| Data Models | ✅ Done | Pydantic schemas for all V0 primitives |
| Aiva-lite Router | ✅ Done | 3 simulated route candidates |
| Aiva-lite Scorer | ✅ Done | Composite utility, urgency-weighted |
| Aiva-lite Selector | ✅ Done | Winner selection + human rationale |
| Rail-lite Executor | ✅ Done | 5-state machine, validated transitions |
| Cloked-lite Logger | ✅ Done | SHA-256 hash chain, tamper detection |
| FastAPI (5 endpoints) | ✅ Done | Full V0 request loop |
| Test Suite (10 tests) | ✅ Done | Routing, scoring, states, chain integrity |
| CI (GitHub Actions) | ✅ Done | Runs on every push |

### Phase 1 — Full Graph Engines

| Component | Status | Details |
|-----------|--------|---------|
| Medical Risk Engine | ✅ Done | Deterministic thermal decay |
| Volatility Engine | ✅ Done | FX-safe scoring & rejection |
| Compliance Engine | ✅ Done | Sanctions + high-risk handling |
| Liquidity Engine | ✅ Done | Node balance + stress logic |
| AIVA Merge Engine | 🟩 In Progress | Multi‑graph score fusion |
| Rail Executor | ✅ Done | Hops, retries, resilience |
| Structured Events | ✅ Done | JSON logs for each hop |
| Test Suite | ✅ Done | Full risk‑scenario coverage |

---

## 🎯 Next Steps (Phase 2)

- AIVA: Weighted composite scoring  
- Rail: Multi-hop settlement chains  
- Cloked: Evidence capsule encryption  
- API Layer: Public routing endpoint  
- CLI Tool: lupctl for running transactions  

---

## 📜 License
Internal experimental research prototype.
Trademark Chris Gogoi

