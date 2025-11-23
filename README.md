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

## © 2025 Lupine Systems
