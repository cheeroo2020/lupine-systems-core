# CLAUDE.md — Lupine Systems

> Canonical context for AI coding agents in this repo.
> **Rule of precedence: the code in `src/` is ground truth.** This file describes what
> exists today (V0) and, separately, the longer-term vision from "The Lupine Systems Book"
> (a 239-page internal doc that is NOT in this repo). Never assume book features are
> implemented — Section 5 lists what's real, Section 6 is the north star only.

---

## 1. What Lupine is

> Lupine decides how value moves when the cost of getting it wrong is high.

Deterministic infrastructure for cross-border value movement. Legacy correspondent banking
is non-deterministic (static routing, treasury-driven corridors, reactive compliance) →
unpredictable delays, surprise escalations, hidden FX exposure. Lupine replaces "push and
hope" with predictive routing, observable execution, and cryptographic evidence.

Primary corridor: **Australia → Singapore (AUD→SGD)**.

---

## 2. The three layers (keep these boundaries clean)

Three layers, hard rule: **no layer leaks logic upward, no layer assumes another's job.**

| Layer | Role | V0 module |
|-------|------|-----------|
| **Aiva** | Intelligence — score routes, pick winner | `src/aiva_lite/` |
| **Lupine Rail** | Execution — state machine, hop progression | `src/rail_lite/` |
| **Cloked** | Evidence — cryptographic audit log | `src/cloked_lite/` |

V0 implementations carry the `_lite` suffix — they are deliberately simplified versions of
the full-fledged layers. Keep the suffix; don't rename to drop it.
`Cloked` is spelled deliberately (not "Cloaked"). Do not "correct" it.

Flow: **Aiva → Rail → Cloked**, with every step also logged to Cloked.

---

## 3. V0 — what actually exists (GROUND TRUTH)

V0 is the first working loop: take a movement request → score route options → pick the best
→ simulate execution → produce a tamper-evident evidence log. **Payments only.**

### Module map
```
src/
├── models/schemas.py        # Pydantic models for all V0 primitives
├── aiva_lite/
│   ├── router.py            # generate 3 candidate routes (Fast, Cheap, Balanced) — simulated
│   ├── scorer.py            # composite utility, urgency-weighted
│   └── selector.py          # pick winner + human-readable rationale
├── rail_lite/executor.py    # 5-state machine, validated transitions
├── cloked_lite/logger.py    # SHA-256 hash chain + verify_chain()
└── api/main.py              # FastAPI, 5 endpoints
tests/  test_aiva.py · test_rail.py · test_cloked.py   (10 tests)
docs/   v0_spec.md · guide.md (plain-English guide)
```

### Aiva-lite scoring (this is the real model — only THREE factors)
```
U = w1·Speed + w2·Cost + w3·Reliability
```
Scores normalised 0→1 (e.g. speed = 1 − time/max_time, cost = 1 − cost/max_cost).
Weights shift by `urgency`:

| urgency  | speed | cost | reliability |
|----------|-------|------|-------------|
| low      | 15%   | 55%  | 30%         |
| normal   | 25%   | 35%  | 40%         |
| high     | 50%   | 15%  | 35%         |
| critical | 60%   | 5%   | 35%         |

Highest U wins; selector emits the winner plus a plain rationale. **Do not** silently expand
this to the book's 7-score model — that's a future step, not a bug to fix.

### Rail-lite state machine
```
initiated → scored → route_selected → executing → completed
                                       executing → failed
```
Invalid transitions raise `ValueError`. The machine enforces every step.

### Cloked-lite evidence chain
Append-only SHA-256 hash chain from a `genesis` entry; each entry stores `prev_hash`.
`verify_chain()` recomputes every hash and checks linkage — any tamper returns `False`.
Logged events: `request_created`, `routes_generated`, `routes_scored`, `execution_completed`.

### API — 5-step flow (`src/api/main.py`)
1. `POST /create-movement` (amount, from_currency, to_currency, urgency) → `request_id`
2. `GET  /get-routes/{request_id}` → 3 route options
3. `POST /score-routes/{request_id}` → selected route + scores
4. `POST /execute/{request_id}` → status + state history
5. `GET  /log/{request_id}` → full evidence log + `chain_valid`

### Run
```
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```
CI runs on every push (GitHub Actions). Deploy config: `render.yaml`.

---

## 4. Working agreements for changes

- Match existing module/layer placement; respect the three-layer boundary.
- New logic ships with tests (mirror `tests/test_{aiva,rail,cloked}.py`); keep CI green.
- Keep V0 honest: simulated where it says simulated. Don't fake depth.
- If a change implies a new event, add it to the Cloked log and to `verify_chain` coverage.

---

## 5. The book's full vision (NORTH STAR — not yet built)

Reference for *direction*, not current behaviour. Don't implement unless explicitly asked.

- **Aiva full model:** seven weighted graphs (Hop, Corridor, Liquidity, Volatility,
  Compliance, Failure, Medical) feeding a 7-term utility:
  `U = α1·Liquidity + α2·Latency + α3·FXCost + α4·Reliability + α5·Compliance + α6·ExposureRisk + α7·MedicalUrgency`.
  V0's 3-factor model (Speed/Cost/Reliability) is the seed of this.
- **FX cost** decomposes to `S0 + ΔS + C + D + V + L`; **exposure risk** = `σ·√t`
  (volatility × √settlement-time); **failure probability** = `1 − (1−L)(1−C)(1−R)` with
  pre-routing pruning; route selection by **Pareto-frontier dominance** with a fallback tree.
- **Rail full model:** idempotent events, per-hop compliance/custody/time-window gates,
  **Payment Trains** (rollback + replay forward to avoid domino failures), multi-level
  intelligent retries, OpenTelemetry-style hashed tracing.
- **Cloked full model:** immutable `LedgerBlock`s, **SCAR** records (graded 1–5),
  externally anchorable **audit capsules**. V0's hash chain is the seed of this.
- **AKO (AivaKnowledgeObject):** the atomic, self-evidencing decision record Aiva will emit.

---

## 6. Out of scope for V0 (do NOT build unless explicitly asked)

The book includes a biological / medical logistics extension (organ viability, cold-chain,
custody, HBML/TGA/FDA, "Deterministic Biological Movement Engine"). It is a future direction,
**not part of V0**. Ignore the MedicalUrgency path and medical graphs unless a task names them.

---

## 7. Conventions

- **Container-style naming:** names gain meaning through the product, they don't describe
  function (Lupine, Aiva, Rail, Cloked, Keel, Cairn). Don't "clarify" them into functional names.
- **Two themes, by surface.** Essays and the revision handbook stay light (paper ground, serif).
  The **lesson slides use the Lupine Command theme**: dark `#0A0A0A` ground, `#E2E8F0` text, Inter
  for prose, JetBrains Mono for all numbers, equations, scores and route data. Cyan `#00E5FF` is
  reserved for the winning route and the final score; red `#FF3366` for failure states and time
  limits. Nothing else uses either colour. Square corners, 1px grid borders, linear transitions,
  no easing or overshoot.
- Preserve the `Cloked` spelling and the `_lite` suffixes.
- Determinism, idempotency, verifiable evidence are values, not features — prefer reproducible,
  auditable designs.

## 8. Going deeper
Always-loaded summary is this file. For more: read `docs/v0_spec.md` and `docs/guide.md`.
For the underlying math/structures (hazard functions, Bayesian failure propagation, full AKO),
ask for a `docs/lupine-architecture.md` to be generated — don't infer details not stated here.
