# Lupine Systems — Plain English Guide

> If you've ever wired money internationally and wondered *why did that take 3 days and cost $40*, Lupine is the answer to that problem.

---

## What is Lupine?

Lupine is a **movement decision engine**.

When someone needs to move a large amount of money from one country to another — say, $500,000 from Australia to Singapore — there are usually several ways to do it. Different banks, different intermediaries, different routes. Each route has a different:

- **Speed** — how long it takes to arrive
- **Cost** — fees and currency conversion charges
- **Reliability** — how likely it is to succeed without issues

Lupine's job is to **look at all the options, score them, pick the best one, and prove it made the right choice**.

It is not a bank. It doesn't hold money. It decides *how* money should move — and leaves a verifiable paper trail of every decision it makes.

---

## Why does this matter?

Most payment systems today are black boxes. You send money, it disappears for a few days, and eventually arrives (or doesn't). Nobody tells you:

- Which route it took
- Why that route was chosen
- What alternatives existed
- What would have happened if something went wrong

This is fine for sending $50 to a friend. It is **not fine** when you're moving $500,000 for a business, a hospital, or a critical supply chain.

Lupine is built for the high-stakes version of this problem.

---

## The three parts of Lupine

Lupine has three layers, each with a specific job:

```
┌─────────────────────────────────────────────────┐
│                   AIVA                          │
│         "What's the best route?"               │
│   Generates options → Scores them → Picks one  │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│                   RAIL                          │
│         "Execute the movement"                  │
│   Moves through states → Tracks every step     │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│                  CLOKED                         │
│         "Prove what happened"                   │
│   Records every event → Locks it with a hash   │
└─────────────────────────────────────────────────┘
```

### AIVA — The brain

AIVA looks at a movement request and asks: *what are my options, and which is best?*

It generates candidate routes (e.g. direct transfer, via USD, via a regional pool), then scores each one across three dimensions:

| Dimension | What it means |
|-----------|---------------|
| Speed | How fast does the money arrive? |
| Cost | How much does it cost in fees? |
| Reliability | How likely is this route to succeed? |

The weighting between speed, cost, and reliability shifts based on **urgency**. If it's critical, speed matters most. If there's no rush, cost matters most.

AIVA then picks the winner and writes a plain-English explanation of why.

**Example output:**
> *"Balanced Route selected. Composite score: 0.849. Beat Fast Route by 0.020 (6h vs 2.5h, 28bps vs 45bps). Weights favoured speed (50%), cost (15%), reliability (35%)."*

### RAIL — The executor

Once AIVA has chosen a route, RAIL executes the movement.

Think of it like a conveyor belt with checkpoints. The movement passes through defined states in order:

```
initiated → scored → route selected → executing → completed
```

It can't skip steps. It can't go backwards. If something goes wrong, it fails cleanly and records exactly where and why.

In V0, this is simulated. In a real deployment, each state would correspond to an actual action — locking funds, sending to a correspondent bank, confirming receipt.

### CLOKED — The evidence layer

CLOKED records everything that happens and **makes it tamper-proof**.

Every event — the request being created, routes being scored, the execution completing — gets hashed using SHA-256 (the same technology used in blockchain). Each new record is linked to the previous one, forming a chain.

If anyone tries to change a record after the fact — even by one character — the chain breaks and verification fails.

This means you can prove, to anyone, exactly what happened and when.

---

## How a movement actually works (step by step)

Let's walk through a real example: moving **500,000 AUD to SGD**, urgency **high**.

### Step 1 — Create the request
You tell Lupine what you want to move.

```
POST /create-movement
amount=500000, from=AUD, to=SGD, urgency=high
```

Lupine creates a unique ID for this request and opens the evidence log.

---

### Step 2 — Get routes
Lupine generates the candidate routes for this corridor.

```
GET /get-routes/{request_id}
```

Returns:
| Route | Time | Cost | Reliability |
|-------|-----:|-----:|------------:|
| Fast Route | 2.5h | 45bps | 0.82 |
| Cheap Route | 18.0h | 12bps | 0.71 |
| Balanced Route | 6.0h | 28bps | 0.93 |

---

### Step 3 — Score and select
Lupine scores every route using the urgency-weighted formula and picks the winner.

```
POST /score-routes/{request_id}
```

Because urgency is **high**, speed gets 50% weight. The Balanced Route wins at 0.849 — it's nearly as fast as the Fast Route but significantly more reliable and cheaper.

---

### Step 4 — Execute
Lupine runs the movement through the state machine.

```
POST /execute/{request_id}
```

The movement progresses through every state and completes.

---

### Step 5 — View the evidence log
Every step is recorded and verified.

```
GET /log/{request_id}
```

Returns the full chain — every event, its timestamp, its hash, and whether the chain is intact. `chain_valid: true`.

---

## What V0 is (and what it isn't)

V0 is the **proof of concept** — the first working loop of the full Lupine vision.

| V0 does | V0 doesn't do (yet) |
|---------|---------------------|
| Score and select routes | Connect to real banks |
| Simulate execution | Process real money |
| Build a tamper-proof evidence log | Encrypt or anchor evidence externally |
| Run live against real FX rates | Handle compliance screening |
| Expose a working API | Support multiple currency corridors |

The routes in V0 are simulated but the **logic is real** — the scoring engine, the state machine, the evidence chain all work exactly as they would in production.

---

## The live data component

Every day, Lupine's automated tests run against the **real AUD/SGD exchange rate** pulled from [Frankfurter](https://www.frankfurter.app) — a free, open exchange rate API backed by the European Central Bank.

This means the daily test record shows you:
- What the AUD/SGD rate was on that day
- How much 500,000 AUD converted to in SGD at that rate
- Whether the full pipeline handled it correctly

Over time, `test-results/` becomes a historical log of both **system health** and **market rates**.

---

## Glossary

| Term | Plain English |
|------|---------------|
| **bps (basis points)** | A unit of cost. 1 bps = 0.01%. 45bps = 0.45% fee. |
| **corridor** | The path money takes between two currencies/countries |
| **composite score** | A single number that combines speed, cost, and reliability |
| **SHA-256** | A mathematical function that turns data into a unique fingerprint. Change anything, the fingerprint changes. |
| **hash chain** | Each record includes the fingerprint of the previous one — tampering breaks the chain |
| **state machine** | A system that moves through defined stages in a fixed order, one at a time |
| **urgency** | How time-sensitive the movement is — affects which route wins |
| **ECB** | European Central Bank — publishes official daily FX reference rates |

---

## Where to find things

```
lupine-systems-core/
│
├── README.md              ← Technical overview with architecture diagrams
├── docs/
│   ├── guide.md           ← This file — plain English explanation
│   └── v0_spec.md         ← V0 specification and success criteria
│
├── src/
│   ├── aiva_lite/         ← AIVA: route generation, scoring, selection
│   ├── rail_lite/         ← RAIL: execution state machine
│   ├── cloked_lite/       ← CLOKED: evidence chain
│   ├── api/               ← The 5 API endpoints
│   ├── data/              ← Live FX rate feed
│   └── models/            ← Data structures
│
├── tests/
│   ├── test_aiva.py       ← Tests for scoring and selection logic
│   ├── test_rail.py       ← Tests for state machine
│   ├── test_cloked.py     ← Tests for evidence chain
│   └── test_live.py       ← Daily live FX integration tests
│
└── test-results/
    ├── README.md          ← How the daily testing works
    └── YYYY-MM-DD.md      ← One file per day, auto-generated
```
