# Lupine Systems — Core Infrastructure (Phase 1)

This repository holds the **Phase 1 technical foundation** of Lupine Systems:

- **Aiva** — deterministic multi-graph intelligence engine  
- **Lupine Rail** — event-driven execution state machine  
- **Cloked** — hash-linked evidence and audit capsule layer  

The objective of Phase 1 is to build a **prototype simulation**, not a production system:

1. Aiva constructs multi-layer weighted graphs  
2. Aiva selects an optimal deterministic route using scoring + Pareto logic  
3. Lupine Rail executes that route hop-by-hop as a state machine  
4. Cloked records each hop as verifiable hash-linked JSON evidence  

---

## 📁 Project Structure

```
lupine-systems-core/
├── docs/              # Architecture diagrams, design notes, Jira mappings
├── notebooks/         # Jupyter notebooks for experiments
├── src/
│   ├── aiva/          # EPIC 1–3: Graphs, scoring, routing
│   ├── rail/          # EPIC 4: Execution state machine
│   └── cloked/        # EPIC 5: Evidence capsule and hash chain
└── tests/             # Minimal tests for validation
```

---

## 🚀 Phase 1 Goals

### ✔ Aiva v0.1 — Multi-Graph Routing Engine  
- Hop Graph  
- Corridor Graph  
- Liquidity Graph  
- Volatility Graph  
- Compliance Graph  
- Failure Graph  
- Medical Urgency Graph  
- Multi-Graph Merge Engine  

### ✔ Scoring Engine v0.1  
- Liquidity Score  
- Latency Score  
- FX Cost Score  
- Reliability Score  
- Compliance Score  
- Exposure Risk  
- Utility Function  

### ✔ Route Selection Engine v0.1  
- Candidate generation  
- Dominance logic  
- Pareto frontier  
- Optimal route + fallback tree  

### ✔ Lupine Rail v0.1  
- State machine (INIT → PRECHECK → HOP_1 → DONE)  
- Hop execution simulator  
- Failover logic  
- Event logs  

### ✔ Cloked v0.1  
- Evidence capsule schema  
- Hash linking  
- Export + replay  

---

## 📦 Installation

```
pip install -r requirements.txt
```

---

## ⚙ Requirements

Developed primarily using:

- Python 3.10+
- networkx
- pandas
- numpy

---

## 🧭 Status

Phase 1 development is underway.  
This repo is the **core technical infrastructure** for the Lupine ecosystem.

---
```
mermaid

graph TD
    %% -- STYLES --
    classDef main fill:#2C3E50,stroke:#fff,stroke-width:2px,color:#fff;
    classDef aiva fill:#8E44AD,stroke:#fff,stroke-width:2px,color:#fff;
    classDef rail fill:#C0392B,stroke:#fff,stroke-width:2px,color:#fff;
    classDef cloked fill:#27AE60,stroke:#fff,stroke-width:2px,color:#fff;
    classDef data fill:#ECF0F1,stroke:#BDC3C7,stroke-width:1px,color:#333;

    %% -- ORCHESTRATOR --
    Orchestrator(main_skeleton.py):::main
    
    %% -- AIVA LAYER --
    subgraph AIVA ["🟣 AIVA (Intelligence Layer)"]
        MergeEngine[merge_engine.py]:::aiva
        HopGraph[hop_graph.py]:::aiva
        MockGraphs[mock_graphs.py]:::aiva
        
        MockGraphs -->|Scores 1.0| MergeEngine
        HopGraph -->|Network Topology| MergeEngine
    end

    %% -- RAIL LAYER --
    subgraph RAIL ["🔴 RAIL (Execution Layer)"]
        Executor[executor.py]:::rail
        StateMachine[state_machine.py]:::rail
        
        Executor -->|Updates| StateMachine
    end

    %% -- CLOKED LAYER --
    subgraph CLOKED ["🟢 CLOKED (Evidence Layer)"]
        Auditor[auditor.py]:::cloked
        EvidenceLog[(Evidence Log)]:::cloked
    end

    %% -- DATA FLOW --
    Orchestrator -->|1. Request Route| MergeEngine
    MergeEngine -->|2. Return Route [NodeA, NodeB]| Orchestrator
    
    Orchestrator -->|3. Execute Route| Executor
    Executor -->|4. Hop Status 'COMPLETED'| Orchestrator
    
    Orchestrator -->|5. Send Evidence| Auditor
    Auditor -->|6. Generate SHA-256 Hash| EvidenceLog

---

## © 2025 Lupine Systems
