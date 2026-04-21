"""
Educational article library for Lupine Systems daily news.

One article per day. The daily workflow picks article N where
N = days since LAUNCH_DATE. When all articles have been published,
the sequence loops back to article 0.

Each article is ~100 words and teaches one concept. Read in order,
they build a complete mental model of the Lupine architecture.
"""
from datetime import date

LAUNCH_DATE = date(2026, 4, 21)

ARTICLES = [
    {
        "title": "Day 1 — What Lupine is, and why",
        "body": """When someone moves half a million dollars across borders, several things have to be decided quickly: which bank chain carries it, how fast it needs to arrive, how much can be lost to fees, and what happens if a step fails.

Today, those decisions are opaque. Banks pick routes behind the scenes with no explanation and no paper trail.

Lupine is a **movement decision engine**. It evaluates route options, scores them on speed, cost, and reliability, picks the best one, executes it through a strict state machine, and leaves a tamper-proof evidence chain proving every decision.

It's built for high-stakes transfers where getting it wrong is expensive.""",
    },
    {
        "title": "Day 2 — The three-layer architecture",
        "body": """Lupine splits its work across three specialised layers, each with a single responsibility.

**AIVA** is the intelligence layer. It looks at a movement request, generates candidate routes, scores them, and picks a winner. It answers the question *which route is best?*

**RAIL** is the execution layer. It runs the chosen route through a strict state machine — initiated, scored, route selected, executing, completed. It enforces order and catches failures.

**CLOKED** is the evidence layer. Every event across AIVA and RAIL gets hashed, chained, and made tamper-proof. It answers the question *prove this actually happened.*

Separation of concerns keeps each layer simple and verifiable.""",
    },
    {
        "title": "Day 3 — Meet AIVA, the intelligence layer",
        "body": """AIVA does three jobs, each handled by a separate module.

**router.py** generates candidate routes. For V0 it returns three options per corridor: a Fast Route, a Cheap Route, and a Balanced Route. In production, this would query live liquidity and corridor data.

**scorer.py** evaluates each candidate using the composite utility function — a weighted blend of speed, cost, and reliability. The weights shift based on urgency.

**selector.py** picks the winner (highest composite score) and writes a plain-English rationale explaining why it beat the alternatives.

The output is a decision plus a paper trail. Every score and weight is preserved for the evidence log.""",
    },
    {
        "title": "Day 4 — Why three routes",
        "body": """AIVA generates exactly three route options for every request: Fast, Cheap, and Balanced.

This isn't arbitrary. Three is the smallest number that makes scoring meaningful — with two options you're only comparing; with three you can see a trade-off spectrum.

**Fast Route** optimises for arrival time. Expensive, reasonably reliable.
**Cheap Route** optimises for cost. Slow, slightly less reliable.
**Balanced Route** is a compromise on both, but typically has the highest reliability.

With three options, the scoring engine has enough variety to show clear winners under different urgency profiles. It also mirrors how a human broker would think: *what's fastest, what's cheapest, what's safest?*""",
    },
    {
        "title": "Day 5 — The composite utility function",
        "body": """Every route gets a single composite score between 0 and 1. Higher is better.

The formula:

**U = w₁·Speed + w₂·Cost + w₃·Reliability**

Where:
- **Speed** = 1 − (route_time / max_route_time), so faster = higher
- **Cost** = 1 − (route_cost / max_route_cost), so cheaper = higher
- **Reliability** = already 0–1, direct score

The weights (w₁, w₂, w₃) always sum to 1.0 and shift based on urgency.

Because every dimension is normalised to the same 0–1 scale before weighting, the scores are directly comparable across routes. The winner is simply the route with the highest composite score — no ambiguity, no subjective judgement.""",
    },
    {
        "title": "Day 6 — Urgency weights",
        "body": """Not every movement has the same priority. Lupine uses four urgency levels, each with its own weight profile:

| Urgency  | Speed | Cost | Reliability |
|----------|------:|-----:|------------:|
| low      |  15%  |  55% |         30% |
| normal   |  25%  |  35% |         40% |
| high     |  50%  |  15% |         35% |
| critical |  60%  |   5% |         35% |

Low urgency favours the Cheap Route. Critical urgency almost forces the Fast Route. Reliability stays significant at every level because failed transfers are always costly.

These profiles aren't set in stone. In production they'd be tunable per client or per corridor. But the mechanism — urgency-driven weight shifts — is the core of how Lupine adapts decisions to context.""",
    },
    {
        "title": "Day 7 — Basis points, explained",
        "body": """Route costs in Lupine are expressed in **basis points** (bps), not percentages.

**1 bps = 0.01%** — a hundredth of one percent.

So a 45 bps fee on 500,000 AUD works out to:

500,000 × 0.0045 = **2,250 AUD**

Why basis points instead of percentages? Financial professionals deal in very small rate differences constantly. Saying *"we saved 17 bps"* is clearer than *"we saved 0.17%"* when the numbers matter.

The three V0 routes use 45 bps (Fast), 28 bps (Balanced), and 12 bps (Cheap). On a 500k transfer that's a spread between 600 AUD and 2,250 AUD in fees — a real decision worth making carefully.""",
    },
    {
        "title": "Day 8 — Why reliability matters",
        "body": """Speed and cost are visible up front. Reliability is the hidden dimension.

In Lupine, reliability is a score between 0 and 1 representing the historical probability that a route completes successfully without intervention.

- Fast Route: 0.82 (fast but uses fewer redundant links)
- Cheap Route: 0.71 (more hops, more failure points)
- Balanced Route: 0.93 (well-tested, redundant paths)

A failed transfer isn't free. It means stranded funds, recovery calls, delayed settlement, sometimes lost counterparty trust. That's why reliability holds 30–40% weight even when speed matters most.

Lupine's scoring treats reliability as a real cost — not an afterthought.""",
    },
    {
        "title": "Day 9 — Meet RAIL, the execution layer",
        "body": """Once AIVA has picked a route, RAIL runs it.

RAIL is a **state machine**. It moves a movement through five states in a fixed order:

1. **initiated** — request received
2. **scored** — routes evaluated
3. **route_selected** — winner chosen
4. **executing** — movement in progress
5. **completed** (or **failed**) — final state

You cannot skip a state. You cannot go backwards. Trying either raises an error.

Why so strict? Because financial movements must happen in a predictable order. No state machine means race conditions, partial updates, money stuck mid-route. Lupine refuses to allow that by making the legal paths explicit and narrow.""",
    },
    {
        "title": "Day 10 — Why invalid transitions fail",
        "body": """RAIL's state machine rejects any transition that isn't on its explicit allow-list. Try to jump from `initiated` straight to `completed`? It raises a `ValueError`.

This is a design choice, not a limitation.

In a real payments context, the difference between *movement initiated* and *movement completed* might involve locking liquidity, reserving rails, confirming correspondent acknowledgements, and reconciling. Each of those produces events and evidence.

Letting code skip states would let bugs or attackers mark money as *delivered* without it actually moving.

By making the state machine strict, Lupine guarantees that the evidence chain accurately reflects what happened — no silent shortcuts, no invisible steps.""",
    },
    {
        "title": "Day 11 — Meet CLOKED, the evidence layer",
        "body": """CLOKED is Lupine's memory. Every significant event — a request created, routes generated, a route scored, a movement executed — gets recorded with a cryptographic seal.

Each record is a small JSON object containing:
- A sequence number
- An event type
- The payload (the actual data)
- A hash of itself
- The hash of the previous record

That last field is what makes it a **chain**. Tampering with any record changes its hash, which breaks the link to the next record, which breaks the link after that, and so on — until verification fails.

It's a mini blockchain, scoped to one movement.""",
    },
    {
        "title": "Day 12 — SHA-256 explained",
        "body": """SHA-256 is a mathematical function that turns any piece of data into a unique 64-character fingerprint.

Two key properties:
1. **Same input → same output, always.** Run it a billion times, you get the same hash.
2. **Change anything → completely different output.** Flip one bit in a 10MB file, the hash is entirely different.

It's one-way — you cannot reverse a hash back to the original data. But given the data, you can always recompute and check.

Lupine uses SHA-256 on every evidence entry. When you call `verify_chain()`, it recomputes every hash and compares it to the stored one. Any mismatch means tampering.""",
    },
    {
        "title": "Day 13 — Tamper detection in action",
        "body": """Imagine someone breaks in and changes an evidence record — say, altering the payload of entry 2 to hide a failed execution.

The old hash of entry 2 was `a3f9…`. The new payload produces a different hash, `b7e1…`.

But entry 3 still stores `previous_hash = a3f9…` — it was written before the tampering.

When `verify_chain()` runs, it sees entry 3 pointing at `a3f9…`, looks at entry 2, computes its actual hash (`b7e1…`), and detects the mismatch.

Result: chain marked invalid. The tampering is caught immediately.

You don't need to trust storage. You only need to trust the math.""",
    },
    {
        "title": "Day 14 — The genesis link",
        "body": """Every evidence chain starts with a special link: `"genesis"`.

The very first entry has no previous hash — there's no record before it. So instead of chaining to a real hash, it chains to the literal string `"genesis"`.

This gives every chain a fixed, predictable starting point. Verification knows: *if I'm checking entry 0, its previous_hash must be "genesis"*.

It's a small thing, but it solves an edge case cleanly. Without it, the chain would have an ambiguous start — and ambiguity in security systems creates bugs.

Every chain in Lupine traces back to the same two-syllable word.""",
    },
    {
        "title": "Day 15 — The five API endpoints",
        "body": """Lupine V0 exposes a minimal API — just five endpoints that mirror the five steps of a movement:

1. **POST /create-movement** — submit a new request
2. **GET /get-routes** — generate candidate routes
3. **POST /score-routes** — score and pick a winner
4. **POST /execute** — run the execution state machine
5. **GET /log** — retrieve the full evidence chain

Each call corresponds to one step. They have to be called in order because each depends on the state of the previous.

This is deliberate: the API makes the process visible and teachable. Someone using Lupine for the first time can watch each step produce its output, then see how it all comes together in the final log.""",
    },
    {
        "title": "Day 16 — What V0 proves",
        "body": """V0 isn't production. It doesn't talk to real banks, doesn't move real money, and its route catalogue is simulated.

But it proves the **loop closes**.

Every piece of the end-to-end flow works: a request comes in, gets scored against real scoring logic, gets executed through a real state machine, and produces a real cryptographic evidence chain that passes verification.

That matters because the hard parts of the architecture — the scoring engine, the state machine, the hash chain — are not the parts that need swapping out to go to production. The routes and execution backends are.

V0 = the core logic, production-ready. The rest is integration.""",
    },
    {
        "title": "Day 17 — V0 vs a real deployment",
        "body": """What would change between V0 and a production deployment?

| Layer | V0 | Production |
|-------|----|------------|
| Routes | 3 hardcoded | Live graph of bank corridors |
| FX | Live (Frankfurter) | Live (multi-provider, SLA-backed) |
| Execution | Simulated states | Real bank API calls |
| Evidence | In-memory chain | Chain anchored to external ledger |
| Compliance | Not present | Sanctions, KYC, AML checks |
| Persistence | Memory only | Durable database |

The interfaces stay the same. A movement request looks identical. The state machine transitions identically. The evidence chain has the same structure.

That's the point of clean separation: V0 is production in miniature.""",
    },
    {
        "title": "Day 18 — Live FX data",
        "body": """Every day, Lupine's automated tests fetch the live AUD/SGD exchange rate from the [Frankfurter API](https://www.frankfurter.app) — a free, open feed backed by European Central Bank reference rates.

Why live data in a test suite? Two reasons.

**First**, it catches integration issues early. If the FX provider changes its API or returns unexpected data, the daily test fails and opens an issue automatically.

**Second**, it turns `test-results/` into a historical ledger. Look at any past daily file and you can see what the AUD/SGD rate was on that day, plus the full test outcome.

Tests become living records, not just pass/fail checks.""",
    },
    {
        "title": "Day 19 — Deterministic vs live tests",
        "body": """Lupine runs two test suites, and the distinction matters.

**Deterministic tests** (`test_aiva.py`, `test_rail.py`, `test_cloked.py`) use hardcoded inputs. Same data every time. They catch regressions — if someone changes the scoring formula and the answers shift, the tests fail immediately.

**Live tests** (`test_live.py`) pull real market rates. The rate changes daily. These test that the system works against real, moving inputs — that network calls succeed, that external APIs return usable data, that the pipeline handles whatever today's numbers are.

Both matter. Deterministic tests protect the logic. Live tests protect the integrations.

Together they give coverage of both *is the code correct* and *does it still work in the real world.*""",
    },
    {
        "title": "Day 20 — The movement request lifecycle",
        "body": """A single movement request travels through every layer of Lupine. Here's the full arc:

1. **Created** — MovementRequest object with amount, currencies, urgency. Evidence chain opened.
2. **Routed** — 3 candidate routes generated by Aiva-lite.
3. **Scored** — Each route gets speed/cost/reliability scores. Composite utility calculated.
4. **Selected** — Winner picked. Rationale written.
5. **Executed** — Rail-lite state machine runs through all 5 states.
6. **Logged** — Every step appended to the evidence chain as it happens.
7. **Verified** — `verify_chain()` confirms nothing was tampered with.

Every step leaves a trace. At the end, you have not just a result but a full auditable history.""",
    },
    {
        "title": "Day 21 — Pydantic schemas",
        "body": """Every data object in Lupine is defined as a **Pydantic schema** in `src/models/schemas.py`.

Pydantic enforces types at runtime. If code tries to create a `MovementRequest` with `amount="five hundred thousand"` instead of `500000`, Pydantic rejects it immediately with a clear error.

Why use Pydantic? Because financial systems break catastrophically when a string creeps in where a number was expected. Silent type coercion hides bugs. Explicit validation surfaces them at the boundary where they originated.

Every `RouteOption`, `DecisionScore`, `ExecutionState`, `EvidenceEntry` — they're all validated on creation. Invalid data never makes it into the system.""",
    },
    {
        "title": "Day 22 — The rationale output",
        "body": """When AIVA picks a winner, it doesn't just return the route — it writes a **plain-English rationale**.

Example:

> *"Balanced Route selected via AUD → SGD (Tier 2 regional). Composite score: 0.849. Beat Fast Route by 0.020 (6h vs 2.5h, 28bps vs 45bps). Weights favoured speed (speed=50%, cost=15%, reliability=35%)."*

This matters because financial decisions often need to be defended. A regulator, an auditor, or a client asking *why did you pick this route?* gets a clear answer — not just a number.

The rationale is generated deterministically from the same data as the score, so it's always consistent with the decision.""",
    },
    {
        "title": "Day 23 — Why in-memory storage in V0",
        "body": """V0 stores movement state in a Python dictionary — no database, no persistence.

Why? Because V0 is about proving the decision logic works, not demonstrating durability.

Adding a database introduces tradeoffs — schema migrations, connection pooling, backup strategies. Those are real engineering problems, but they're separate from *does the scoring engine score correctly?*

When V1 comes, the storage layer will be swapped for something durable (likely Postgres for state, S3 or a ledger for evidence). The rest of the code won't change — the scoring, state machine, and evidence chain are all storage-agnostic.

V0's in-memory simplicity is a feature, not a shortcut.""",
    },
    {
        "title": "Day 24 — The daily health check",
        "body": """Every day at 9am UTC, GitHub Actions runs the full Lupine test suite automatically.

Fourteen tests cover every layer:
- 10 deterministic tests (scoring, state machine, evidence chain)
- 4 live FX tests (real market rate integration)

After each run, the workflow writes a dated Markdown file to `test-results/`, commits it, and pushes it back to the repo.

If any test fails, it automatically opens a GitHub Issue with a link to the failed run.

Nobody has to remember to run the tests. Nobody has to check a dashboard. The system tests itself every day and leaves a written record of every check.""",
    },
    {
        "title": "Day 25 — What the evidence log proves",
        "body": """At the end of a movement, Lupine's evidence log proves three things:

**1. What happened.** Every event — request, scoring, selection, execution — is recorded with its data.

**2. When it happened.** Each entry has a timestamp.

**3. That the record is authentic.** The hash chain makes silent tampering mathematically detectable.

This isn't about blockchain hype — it's about accountability. For a high-stakes transfer, *"the money arrived"* is not enough. You want: *"here's the route we considered, here's why we picked this one, here's the chain of states we moved through, and here's proof none of it has been altered."*

That's what the evidence log delivers.""",
    },
    {
        "title": "Day 26 — Why Frankfurter for FX",
        "body": """Of all the FX APIs available, Lupine uses **Frankfurter**. Why?

- **Free.** No API key, no rate limit surprises.
- **ECB-sourced.** Rates come from the European Central Bank daily reference rates — trustworthy, auditable.
- **Simple.** One HTTP call, clean JSON response, no authentication dance.
- **Stable.** Public project, minimal breaking changes.

For production, you'd want redundancy — probably multiple providers with fallback logic and SLA guarantees. Frankfurter alone wouldn't cover that.

But for V0's daily health check, it's ideal: zero setup friction, real data, and a stable interface. It lets Lupine test its live integration path without introducing complexity that isn't the point of V0.""",
    },
    {
        "title": "Day 27 — The observer role",
        "body": """Lupine never *initiates* a movement — it only **evaluates and records** them. That's a deliberate philosophical choice.

In most payment systems, the routing engine is also the executor. That means a bug in routing can cause a real movement to go wrong.

In Lupine, AIVA's output is advisory by default. RAIL simulates (in V0) or orchestrates (in production) — it doesn't hold funds. CLOKED only observes and records.

This separation means you can drop Lupine into an existing payment network as a *decision adviser and audit trail* without giving it custody over any funds.

It's an architectural pattern: observer, not actor.""",
    },
    {
        "title": "Day 28 — Structured events",
        "body": """Every significant thing that happens in Lupine is a **structured event** — a JSON-shaped record with a fixed schema.

Not a log message. Not a print statement. A record.

This matters because logs rot. People read them once, then throw them away. Events are queryable. You can ask *"show me every time a Fast Route beat a Balanced Route in the last 30 days"* and get an answer from the evidence trail.

Every RouteOption, DecisionScore, ExecutionState, and EvidenceEntry is structured this way. The system produces data, not prose.

When Lupine grows, this structural foundation is what allows analytics, dashboards, and machine learning to plug in naturally.""",
    },
    {
        "title": "Day 29 — Why it's called Lupine",
        "body": """The name comes from *Canis lupus* — the wolf. Wolves are pack animals that move deliberately, coordinate tightly, and hunt at the edges of risk.

Lupine Systems borrows that image. It's meant to handle movements at the edges of risk — transfers that are large, urgent, or sensitive enough that casual decisions are dangerous.

Each layer (AIVA, RAIL, CLOKED) plays a role in the pack: intelligence, execution, memory. They coordinate. None works alone.

And like a pack, the system values proof over trust. A wolf reads the ground for evidence — prints, scat, disturbed brush. Lupine reads the evidence chain.""",
    },
    {
        "title": "Day 30 — Where Lupine goes next",
        "body": """V0 closes the loop. V1 starts filling it in.

Coming next:
- **Real corridor data.** Live graphs of bank-to-bank connections, liquidity per node, latency per hop.
- **Multi-hop routing.** Movements that pass through 2, 3, or more intermediaries — optimising across chains, not single routes.
- **Compliance engine.** Automated sanctions screening, KYC checks, AML flags before a route is even scored.
- **Persistent evidence.** Chains anchored to an external ledger so tampering is impossible even if Lupine itself is compromised.
- **Medical payload logic.** Time-sensitive physical movements (organs, samples) where delays cause irreversible damage.

The architecture is built to grow into all of it without changing the core.""",
    },
]

