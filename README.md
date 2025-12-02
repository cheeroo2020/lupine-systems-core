Lupine Systems — Core Infrastructure (Phase 1)

"When the stakes are human, failure cannot be probabilistic."

This repository holds the Phase 1 technical foundation of Lupine Systems:

Aiva: Deterministic multi-graph intelligence engine (The Brain).

Lupine Rail: Event-driven execution state machine (The Muscle).

Cloked: Hash-linked evidence and audit capsule layer (The Truth).

The objective of Phase 1 is to build a walking skeleton simulation that enforces the Biological Movement Contract (BMC):

Aiva selects a route based on Medical, Financial, and Regulatory constraints.

Rail executes the route hop-by-hop with resilience and retry logic.

Cloked cryptographically logs the events for immutable audit trails.

📁 Project Structure

lupine-systems-core/
├── docs/              # Architecture diagrams, Jira mappings
├── src/
│   ├── aiva/          # Intelligence Layer (Graphs & Routing)
│   │   ├── hop_graph.py        # Network topology
│   │   ├── medical_graph.py    # Thermal decay & viability logic
│   │   ├── volatility_graph.py # FX risk & market crash protection
│   │   ├── liquidity_graph.py  # Nostro balance checks
│   │   ├── compliance_graph.py # Sanctions & blacklist logic
│   │   └── merge_engine.py     # Central routing brain
│   ├── rail/          # Execution Layer
│   │   ├── executor.py         # Hop simulator with Retry/Failover
│   │   └── state_machine.py    # Transaction Lifecycle (LOCKED -> SETTLED)
│   └── cloked/        # Evidence Layer
│       └── auditor.py          # SHA-256 Hashing logger
├── tests/             # Verification Suite
│   └── test_risk_scenarios.py  # A/B/C/D/E Scenario Tests
├── main_skeleton.py   # Entry Point
├── requirements.txt   # Dependencies
└── README.md          # This file


🧬 System Architecture (The Steel Thread)

This diagram represents the flow of data in the current build.

graph TD
    %% Nodes
    Orchestrator(main_skeleton.py)
    
    subgraph AIVA [🟣 AIVA Intelligence]
        MergeEngine[merge_engine.py]
        RiskGraphs[Risk Graphs]
        
        RiskGraphs -->|Medical/FX/Legal Scores| MergeEngine
    end

    subgraph RAIL [🔴 RAIL Execution]
        Executor[executor.py]
        StateMachine[state_machine.py]
        
        Executor -->|Update State| StateMachine
        Executor -->|Retry Logic| Executor
    end

    subgraph CLOKED [🟢 CLOKED Truth]
        Auditor[auditor.py]
        EvidenceLog[(Evidence Log)]
    end

    %% Flow
    Orchestrator -->|1. Request Route| MergeEngine
    MergeEngine -->|2. Return Safe Route| Orchestrator
    
    Orchestrator -->|3. Execute Transaction| Executor
    Executor -->|4. Status: SETTLED| Orchestrator
    
    Orchestrator -->|5. Log Evidence| Auditor
    Auditor -->|6. SHA-256 Hash| EvidenceLog


(Note: If the diagram above does not render, view this file on GitHub.com or use a Markdown viewer with Mermaid support.)

🚀 Phase 1 Progress

🟣 Aiva v0.1 (The Risk Engine)

[x] Hop Graph (Basic Topology)

[x] Merge Engine (Routing Logic)

[x] Medical Graph (Thermal Decay Logic) — Story 1.7

[x] Volatility Graph (Market Crash Protection) — Story 1.4

[x] Compliance Graph (Sanctions Screening) — Story 1.5

[x] Liquidity Graph (Nostro Balance Checks) — Story 1.3

🔴 Lupine Rail v0.1 (The Execution Engine)

[x] State Machine (CREATED → LOCKED → IN_FLIGHT → SETTLED) — Story 4.1

[x] Hop Executor (Simulation) — Story 4.2

[x] Failover & Retry Logic (Chaos Monkey Resilience) — Story 4.3

🟢 Cloked v0.1 (The Evidence Engine)

[x] Auditor (Basic Logging)

[x] Hashing (SHA-256)

[ ] Merkle Tree Implementation (Next Sprint)

[ ] JSON Capsule Schema (Next Sprint)

📦 Getting Started

1. Install Dependencies

pip install -r requirements.txt


2. Run the Test Suite

Verify that the system correctly handles all 5 risk scenarios (Medical Spoilage, Market Crashes, Sanctions, Liquidity Crunch, and Happy Path).

python -m unittest tests/test_risk_scenarios.py


3. Run the Main Simulation

This runs the "Steel Thread" with resilience logic enabled.

python main_skeleton.py


<div align="center">





<b>© Lupine Systems</b>





</div>
