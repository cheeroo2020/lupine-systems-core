# Lupine Systems — 14-Day Revision Handbook

**For:** Chris Gogoi · **Start:** 27 Jul 2026 · **Finish:** 9 Aug 2026
**Assumes:** zero memory. No code required. Concepts only.

---

## How to use this

One section per day, ~20 minutes. Every day has the same shape:

1. **The one idea** — the single sentence that day hangs on
2. **The explanation** — read it once, slowly
3. **⚙️ Mechanism** — the precise version of something you previously only half-knew
4. **🎤 Say it like this** — the pitch-ready sentence
5. **✅ Check yourself** — three questions. *Answer out loud before scrolling to the answers.*

**The single most important rule:** say the answers **out loud**, in your own words, before reading them. Reading feels like learning and isn't. Speaking is the test. If you stumble mid-sentence, you've found your gap — reread that section and try again.

### Why there are 12 "mechanisms"

In April you answered 18 comprehension checks. Five were fully right. Twelve came back as *"right direction, but…"*. Those twelve are your entire curriculum — the places where you have the instinct but not the machinery. They're marked ⚙️ throughout. Master those twelve and you own this.

---

## The two tracks

You're mastering two different things and they need different treatment:

- **🧠 Concept track — all 14 days.** The theory. Why Lupine must exist, how each layer thinks. This is the main event.
- **🗂 Repo track — 7 sessions woven across the 14 days.** *Repo literacy, not code fluency.* You're not learning to write Python. You're learning the building's floor plan so you can say **"change the critical-urgency weights"** and know exactly which file that is — and so you can explain your own system to a technical hire or an investor without hand-waving.

Repo sessions are short (10–20 min) and land on days where the concept you just learned is implemented in the file you're about to look at. **Days 1, 4, 6, 7, 10, 13 and 14 have no repo work** — those are heavy theory days, consolidation, or exam.

Full repo track is at the end of this document: **[The Repo Track](#the-repo-track--7-sessions)**.

---

## Your source documents

Two files in `docs/`, same 8 study sessions in both:

| File | Use it for |
|---|---|
| **`lupine_master_study_pack (1).html`** | **Primary.** Open in a browser. Has "Why read / Watch for" notes on every reading that link it back to your theory chapters — the PDF lost these. Richer Adyen/Remitly material. |
| **`Lupine Systems — Study Sessions & Market Readings (1).pdf`** | Backup. Fixed page numbers, good for offline or annotating. |

### Master reading map

| Day | Read in the HTML | PDF pages |
|---|---|---|
| **1** | Part I — Chapters 1–2 · *The Legacy Problem* | 4–6 |
| **2** | Part I — Chapter 3 · *ISO 20022, SWIFT gpi* | 7–10 |
| **3** | Part I — Chapter 4 · *FX Intelligence & Corridor Engineering* | 11–14 |
| **4** | Part II — Chapter 1 · *Deterministic Routing Architecture* | 15–18 |
| **5** | Part II — Chapter 2 · *Scoring Engines* | 19–21 |
| **6** | Part II — Chapter 4 · *Multi-Constraint Optimisation* | 22–24 |
| **7** | *(re-skim your weakest two sessions)* | — |
| **8** | Part III — Chapters 2+3 · *Execution Pipeline, Retries & State Machines* | 25–27 |
| **9** | Part IV — Chapters 1+4 · *Cryptographic Evidence Chains* | 28–30 |
| **10** | *(none — your own system)* | 31 |
| **11** | *(none — your own system)* | — |
| **12** | Wise: *Our Infrastructure* · *Pricing & take rate* · *CEO letter* | 32–42 |
| **13** | Adyen: *Value chain* · *Single platform* · *RevenueAccelerate* · *Failover* · *Data centres*<br>Remitly: *Global network* · *Tech platform deep-dive* · *Hybrid risk model* | 42–61<br>63–78 |
| **14** | *(none — exam)* | — |

**Order matters:** read the source section **first**, then the handbook day. The source gives you the material; the handbook tells you which twelve things you previously got imprecise, and gives you the pitch language.

---

## Animated lessons

Click-through visual versions of each day, hosted on the project's own site. They're a **supplement, not a substitute** — watching is still passive. Use one to *see* a mechanism move, then close it and say the mechanism out loud.

**Live at:** `cheeroo2020.github.io/lupine-systems-core/lessons/`

| # | Lesson | File | Status |
|---|---|---|---|
| 1 | [Why the System Is Broken](https://cheeroo2020.github.io/lupine-systems-core/lessons/01-why-the-system-is-broken.html) | `01-why-the-system-is-broken.html` | ✅ live |
| 2 | [Messaging Is the Real Control Layer](https://cheeroo2020.github.io/lupine-systems-core/lessons/02-messaging-is-the-control-layer.html) | `02-messaging-is-the-control-layer.html` | ✅ live |
| 3 | [Corridors and the Real FX Rate](https://cheeroo2020.github.io/lupine-systems-core/lessons/03-corridors-and-the-real-fx-rate.html) | `03-corridors-and-the-real-fx-rate.html` | ✅ live |
| 4 | [Aiva's Brain — Seven Graphs at Once](https://cheeroo2020.github.io/lupine-systems-core/lessons/04-aivas-brain-seven-graphs.html) | `04-aivas-brain-seven-graphs.html` | ✅ live |
| 5 | [Scoring — How Routes Get Judged](https://cheeroo2020.github.io/lupine-systems-core/lessons/05-scoring-how-routes-get-judged.html) | `05-scoring-how-routes-get-judged.html` | ✅ live |
| 6 | Pareto and Constraints | `06-pareto-and-constraints.html` | — |
| 7 | Consolidation | `07-consolidation.html` | — |
| 8 | RAIL — Making It Actually Happen | `08-rail-making-it-happen.html` | — |
| 9 | CLOKED — Proving It Happened | `09-cloked-proving-it-happened.html` | — |
| 10 | What's Real and What Isn't | `10-whats-real-and-what-isnt.html` | — |
| 11 | Your System as a Demo | `11-your-system-as-a-demo.html` | — |
| 12 | Wise — The Operator Who Built Rails | `12-wise-who-built-their-own-rails.html` | — |
| 13 | Adyen and Remitly — Platform and Network | `13-adyen-and-remitly.html` | — |
| 14 | Cold Exam | `14-cold-exam.html` | — |

**Naming convention:** `NN-topic-in-kebab-case.html`, zero-padded. The padding is what makes numeric and alphabetical order agree — unpadded, `10` sorts before `2` and the directory listing scrambles.

---

# WEEK 1 — THE THEORY

---

## Day 1 — Why the system is broken

> 📖 **Read first:** HTML → *Part I — Chapters 1–2* · PDF pp. 4–6
> 🎬 **Animated lesson:** [1. Why the System Is Broken](https://cheeroo2020.github.io/lupine-systems-core/lessons/01-why-the-system-is-broken.html)
> 🗂 **Repo:** none — pure theory today

### The one idea
> The global payments system was built for a world that didn't need speed, predictability, or proof — so it is **reactive, not predictive**.

### The setup

You want to move **A$500,000 from Australia to Singapore**. Feels like it should be a single hop. It isn't. It's a relay race between institutions that don't share rules, hours, or software.

Real latency on a corridor like this:

| Outcome | Time |
|---|---|
| Best case | 2.5 hours |
| Median | 28–36 hours |
| P95 (1 in 20) | 3–5 days |
| Worst case | 7–11 days |

That spread — 2.5 hours to 11 days for *the same payment* — is the problem. Not the average. **The unpredictability.**

### Payments move through five layers

Money appears to move sideways (Australia → Singapore). The real work happens **vertically**, through five layers, at every single hop:

| Layer | What it does |
|---|---|
| **5 · Compliance** | AML/CTF, sanctions, KYB, travel rule |
| **4 · Settlement** | RTGS, ACH, instant payment systems |
| **3 · Correspondent** | Nostro/vostro accounts, treasury, liquidity |
| **2 · Messaging** | SWIFT MT, gpi, ISO 20022 |
| **1 · Funding** | Accounts, ledgers, balances |

### Correspondent banking is the actual backbone

No bank has an account in every country. So payments **hop** through 1–4+ intermediary banks that *do* have the right relationships. Each hop adds latency, compliance friction, and liquidity risk.

Two words you must know cold:

- **Nostro** — "**our** money held with **them**" (your bank's account at a foreign bank)
- **Vostro** — "**their** money held with **us**"

These are **pre-funded**. Real money sits there in advance, waiting. When a corridor gets busy and that pool runs dry, payments **queue**. Not fail — queue. Invisibly.

### Compliance re-runs at every hop

Every correspondent does its **own** sanctions screening and AML scoring. A payment that's perfectly clean at origin can be flagged by the third bank in the chain for a reason nobody predicted. **This is the number one cause of multi-day delays.**

### Settlement windows never all overlap

| System | Hours (AEST) |
|---|---|
| AU RITS | 08:00 – 18:00 |
| EU TARGET2 | 17:00 – 02:00 |
| US Fedwire | 21:00 – 05:30 |

There is **no moment when all three are open.** Miss a window and your payment sits for 24+ hours doing nothing.

### The nine structural failure modes

Corridor volatility · routing ambiguity · manual review saturation · liquidity siloing · MT message desync · no predictive engine · evidence black holes · biological timing mismatch · **zero determinism**

### ⚙️ MECHANISM #1 — SWIFT does not move money

> **Not:** "SWIFT encapsulates the value information between institutions."
> **But:** SWIFT is a **messaging network** — the postal service, not the cash. It carries *instructions*. The money actually moves through **RTGS systems** (RITS, TARGET2, Fedwire), **nostro/vostro balances**, FX desks and clearing houses. **SWIFT has never moved a single dollar.**

This distinction matters because it locates where the intelligence gap is. SWIFT tells everyone what to do; nothing in the chain decides whether that was the *right* thing to do.

### 🎤 Say it like this
> "A cross-border payment isn't one transaction — it's a relay through four institutions that don't share hours, rules, or software. Legacy systems send it and deal with failures afterwards. Lupine evaluates the routes, predicts the failures, and picks the best path before the money moves."

### ✅ Check yourself
1. Why can the same A$500K payment take 2.5 hours or 11 days?
2. What is a nostro account, and what happens when it runs dry?
3. If SWIFT doesn't move money — what does?

<details><summary>Answers</summary>

1. Different routes, different correspondents, different windows, different compliance interpretations. Nothing precomputes the path — it follows static agreements set years ago.
2. "Our money held with them" — a pre-funded account your bank holds at a foreign bank. When it's exhausted, payments **queue** invisibly until it's topped up.
3. RTGS systems, nostro/vostro balances, FX desks and clearing houses. SWIFT only carries the instructions.
</details>

---

## Day 2 — Messaging is the real control layer

> 📖 **Read first:** HTML → *Part I — Chapter 3* · PDF pp. 7–10
> 🎬 **Animated lesson:** [2. Messaging Is the Real Control Layer](https://cheeroo2020.github.io/lupine-systems-core/lessons/02-messaging-is-the-control-layer.html)
> 🗂 **Repo:** [**R1 — The map**](#r1--the-map-day-2-15-min) *(15 min)*

### The one idea
> Messages aren't data — they're **legal and operational instructions**. Whoever controls the messaging layer controls the system.

### The stack, and where everyone stops

```
User layer        Bank UI, ERP, procurement
API layer         REST, GraphQL, bank APIs      ← most fintechs stop here
Messaging layer   SWIFT MT / ISO 20022 / gpi    ← real control lives here
Settlement layer  RTGS, ACH, SEPA, NPP
Balance layer     Nostro, vostro, ledgers
```

### Three generations

**SWIFT MT103 (legacy, still runs the world).** Free text. Fields get truncated at each hop. Banks interpret them differently. Sanctions engines choke on unstructured data. Hops can silently modify fields.

**ISO 20022 / MX (the structured future).** XML. Machine-readable, schema-validated, predictable, clean for compliance.

**SWIFT gpi (a tracking overlay).** Adds end-to-end tracking, hop-level timestamps, fee transparency.

### gpi is visibility, not intelligence

gpi shows you that your payment **sat at the Singapore correspondent for 90 minutes waiting for liquidity**. What it can't do: predict that would happen, reroute around it, or tell you a different corridor would have been faster.

> **gpi is a rear-view mirror. Aiva is the windshield.**

That single line is one of the strongest things you can say in a room full of payments people.

### The Lupine move on ISO 20022

Banks adopt ISO 20022 for *compliance and data quality*. Lupine uses it as a **semantic graph** — for corridor scoring, routing optimisation, failure simulation, FX exposure modelling, compliance pre-checks, and building evidence.

In Aiva's model, one payment is **six things at once**: a constraint set, a risk vector, a compliance object, a corridor graph node, a time-window object, and a liquidity demand event.

### Why evidence needs ISO 20022

MT103 crams names, addresses and purpose codes together as free text with no programmatic separation. ISO 20022 gives **discrete, labelled, schema-validated fields** — so you can hash individual fields and build verifiable evidence.

> **You can't hash ambiguity.**

### 🎤 Say it like this
> "Most fintechs build on the API layer. The real control sits one level down, in the messaging layer — those messages are legal instructions telling every system in the chain what to do. gpi gave the industry visibility. It didn't give it intelligence."

### ✅ Check yourself
1. Why is gpi "visibility, not intelligence"?
2. Why can't you build cryptographic evidence from MT103?
3. What do banks use ISO 20022 for, versus what Lupine uses it for?

<details><summary>Answers</summary>

1. It timestamps problems after they happen. It can't predict liquidity shortages, prevent compliance blocks, reroute, or score alternatives. Rear-view mirror.
2. Free-text fields with no programmatic separation — you can't isolate and hash a field that has no defined boundary. You can't hash ambiguity.
3. Banks: migration compliance and data quality. Lupine: a semantic graph for corridor scoring, routing, failure prediction and evidence construction.
</details>

---

## Day 3 — Corridors and the real FX rate

> 📖 **Read first:** HTML → *Part I — Chapter 4* · PDF pp. 11–14
> 🎬 **Animated lesson:** [3. Corridors and the Real FX Rate](https://cheeroo2020.github.io/lupine-systems-core/lessons/03-corridors-and-the-real-fx-rate.html)
> 🗂 **Repo:** [**R2 — The data foundation**](#r2--the-data-foundation-day-3-15-min) *(15 min)*

### The one idea
> Payments don't move randomly — they move through **corridors**, and the "exchange rate" you see is only the first of **eight** stacked components.

### What a corridor is

A corridor is a pathway between two currencies — geopolitical, regulatory, and liquidity-dependent. The same payment can take completely different corridors with wildly different outcomes:

- **AUD → SGD → EUR** (via Singapore)
- **AUD → USD → EUR** (via the dollar)
- **AUD → EUR direct** (thin liquidity)

Liquidity sits in tiers: **Tier 1** primary pools (JPM, Citi, UBS, HSBC, Barclays, XTX) → **Tier 2** regional pools (Singapore, Sydney, Hong Kong, Frankfurt, London) → **Tier 3** local rails (RTGS, ACH, SEPA, NPP, fintech pipes).

### The real rate has eight components

> **Effective rate = S₀ + ΔS + F + V + L + C + D + R**

| | Component | Meaning |
|---|---|---|
| S₀ | Interbank spot | What banks trade at, at scale |
| ΔS | Spread | Liquidity provider's margin |
| F | Forward points | Interest rate differential |
| V | Volatility premium | Risk during the movement |
| L | Liquidity premium | Wider spread when the pool is thin |
| C | Corridor cost | Costs unique to this path |
| D | Delay premium | Price impact from latency |
| R | Compliance buffer | Added on high-risk corridors |

Banks rarely expose V, L, C, D or R. Fintechs expose some. **Lupine exposes all eight** at the intelligence layer.

Note the chain reaction: **delay (D) increases volatility exposure (V), which widens the spread (ΔS)**. Slowness isn't just inconvenient — it's literally more expensive.

### ⚙️ MECHANISM #2 — FX exposure grows with the square root of time

> **Not:** "the fastest route might have more spread."
> **But:** **Exposure = σ × √t** (volatility × square root of settlement time).
>
> The **√** is the whole insight. Exposure grows **non-linearly** — the first few hours of delay hurt *more* than the next few. Going from 1h to 4h roughly doubles exposure; 4h to 16h doubles it again. Early delay is disproportionately expensive.

So Aiva isn't picking the fastest route or the cheapest route. It's picking the route with the **lowest total exposure** — the time/volatility combination that does least price damage. **A fast route through a volatile corridor can cost more than a slower route through a stable one.**

### Banks vs fintechs vs Lupine

- **Banks** route on **treasury cost optimisation** — pre-funded nostro balances, existing correspondent agreements. They optimise for *their* cost, not your outcome.
- **Fintechs** avoid correspondents entirely — netting, internal ledgers, local rails.
- **Lupine** evaluates **all** available paths and optimises for **the payment's outcome**.

### Seven corridor failure modes
Liquidity evaporation · regulatory shock · volatility spikes · window misalignment · correspondent collapse · treasury freeze · geopolitical fracture

### 🎤 Say it like this
> "Everyone thinks the FX rate is one number. It's eight stacked components, and banks only show you two of them. We model all eight — including the one nobody prices properly: the cost of delay itself. Exposure scales with the square root of time, so the first hours of a delay are the expensive ones."

### ✅ Check yourself
1. What does the √ in σ√t actually mean for route choice?
2. Name four of the eight FX components banks don't show you.
3. What's the difference between treasury cost optimisation and outcome optimisation?

<details><summary>Answers</summary>

1. Exposure grows non-linearly — early delay costs disproportionately more. So minimising *total exposure* beats minimising raw time or raw cost.
2. Volatility premium (V), liquidity premium (L), corridor cost (C), delay premium (D), compliance buffer (R).
3. Banks are locked into existing correspondent relationships and pre-funded accounts, so they ask "what's cheapest **for us**?" Lupine has no such bias — it evaluates every corridor and picks the best outcome **for the payment**.
</details>

---

## Day 4 — Aiva's brain: seven graphs at once

> 📖 **Read first:** HTML → *Part II — Chapter 1* · PDF pp. 15–18
> 🎬 **Animated lesson:** [4. Aiva's Brain — Seven Graphs at Once](https://cheeroo2020.github.io/lupine-systems-core/lessons/04-aivas-brain-seven-graphs.html)
> 🗂 **Repo:** none — this is the heaviest theory day, keep it clear

### The one idea
> Aiva doesn't look at a payment through one lens. It looks through **seven simultaneously**, then merges them.

### The seven graphs

| Graph | What it maps |
|---|---|
| **Hop** | Which banks can reach which banks (latency + reliability) |
| **Corridor** | FX routes and their liquidity depth, volatility, spread |
| **Liquidity** | Treasury depth at each tier — predicts droughts |
| **Volatility** | Price risk propagation; each edge carries σ |
| **Compliance** | Which regulatory regimes are compatible |
| **Failure** | Failure probabilities, cascading risk (Bayesian) |
| **Medical urgency** | Phase 2 only — not in V0 |

These merge into a **meta-graph**:

> **W = α₁·Liq + α₂·Lat + α₃·Vol + α₄·FX + α₅·Comp + α₆·Fail + α₇·Urg**

### ⚙️ MECHANISM #3 — Simultaneous evaluation means *better decisions*, not faster ones

> **Not:** "sequential is time consuming."
> **But:** Sequential produces **worse decisions**. If compliance screens first and flags the payment, it **stops** — it never reaches the routing engine, which might have found a corridor where that flag never triggers at all.
>
> Sequential means each system decides **in isolation, blind to the others**. Aiva evaluates everything at once, so it can find paths sequential systems would never discover.

Speed is a side effect. **Discovering better paths is the point.**

### ⚙️ MECHANISM #5 — What "deterministic" actually means

> **Not:** "evaluating all parameters simultaneously."
> **But:** **Same inputs → same output. Every single time.** No randomness, no human judgment in the middle.
>
> Legacy systems are **non-deterministic**: two identical payments, sent an hour apart, can take completely different paths for reasons nobody can reconstruct. Aiva's output is **computed, not guessed** — and the outcome is knowable *before* the money moves.

These are two different ideas and you previously merged them. Simultaneous evaluation is *how Aiva computes*. Determinism is *the property of the result*.

> **"We make cross-border payments deterministic."** That is your single strongest sentence. Make sure you can defend the word.

### The execution blueprint

After computing, Aiva hands Rail a deterministic blueprint: optimal corridor path, hop-level timing model, liquidity requirements, compliance probability matrix, FX exposure curve, **fallback tree**, and the evidence anchor map for Cloked. Rail executes it exactly as specified.

### 🎤 Say it like this
> "Legacy routing checks constraints one at a time, so a compliance flag kills a payment that a different corridor would have sailed through. Aiva evaluates seven dimensions simultaneously and outputs a deterministic blueprint — same inputs, same route, every time, knowable before the money moves."

### ✅ Check yourself
1. Why is sequential evaluation worse — beyond being slower?
2. Define "deterministic" in one sentence.
3. What does Aiva hand to Rail?

<details><summary>Answers</summary>

1. Each system decides blind to the others. A compliance flag stops the payment before routing ever gets a chance to find the corridor that avoids the flag entirely.
2. Same inputs always produce the same output — no randomness, no human judgment.
3. An execution blueprint: corridor path, timing model, liquidity needs, compliance matrix, FX exposure curve, fallback tree, evidence anchor map.
</details>

---

## Day 5 — Scoring: how routes get judged

> 📖 **Read first:** HTML → *Part II — Chapter 2* · PDF pp. 19–21
> 🎬 **Animated lesson:** [5. Scoring — How Routes Get Judged](https://cheeroo2020.github.io/lupine-systems-core/lessons/05-scoring-how-routes-get-judged.html)
> 🗂 **Repo:** [**R3 — Aiva**](#r3--aiva-day-5-20-min) *(20 min — the best pairing in the course)*

### The one idea
> The engine never changes. **The weights change.** Same corridors, different urgency, different winner.

### The composite utility function

> **U(R) = α₁·Liq + α₂·Lat + α₃·FX + α₄·Rel + α₅·Comp + α₆·Exp + α₇·Urg**

The four that matter for V0:

| Score | How it's computed |
|---|---|
| **Liquidity** | β₁·Depth + β₂·Stability + β₃·WindowFit + β₄·VolatilityInverse |
| **Latency** | 1 / ExpectedLatency — faster is higher |
| **Reliability** | 1 − P(failure), from a Bayesian model |
| **FX cost + Exposure** | FXCost = S₀+ΔS+C+D+V+L, paired with Exposure = σ√t |

FX cost and exposure are treated as a **pair** because delay increases exposure which increases cost. A cheap-but-slow route can score badly overall.

### ⚙️ MECHANISM #6 — Liquidity is a gatekeeper

> **Not:** "there'd be less constraint to evaluate."
> **But:** A corridor with no liquidity **physically cannot execute the payment.** It doesn't matter if it has perfect latency, the lowest FX cost, and clean compliance — if there's no money in the nostro account, nothing moves.
>
> **It's like scoring a bridge for speed and safety when the bridge isn't there.**

So liquidity is checked **first**, as elimination — not weighed alongside everything else. Aiva removes impossible paths before spending computation scoring them.

### ⚙️ MECHANISM #7 — Weights shift; they never zero out

> **Not:** "at high urgency, cost and reliability aren't considered."
> **But:** They **are** still in the equation — just weighted lower.
>
> A route with a **40% failure probability would still be rejected under critical urgency**, because reliability drags total utility down far enough to lose. Nothing ever gets switched off.

This is the difference between a naive "sort by speed" and a real optimiser — and it's exactly the kind of thing a sharp investor will probe.

### Your V0's actual weights

| Urgency | Speed | Cost | Reliability |
|---|---:|---:|---:|
| low | 15% | 55% | 30% |
| normal | 25% | 35% | 40% |
| high | 50% | 15% | 35% |
| critical | 60% | 5% | 35% |

**Learn this table.** Notice: reliability never drops below 30%. Cost never fully disappears even at 5%.

### Four route tiers

**Optimal** (highest U — selected) · **Admissible** (on the frontier, valid alternatives) · **Fallback** (used if optimal fails) · **Eliminated** (liquidity-starved or too risky — never selected)

### 🎤 Say it like this
> "We don't just pick the fastest route under time pressure — we pick the best **reliability-adjusted** outcome under time pressure. The weights shift with urgency, but nothing ever gets switched off. A fast route with a 40% failure rate still loses."

### ✅ Check yourself
1. Why is liquidity checked before everything else instead of weighted alongside it?
2. At critical urgency, what happens to cost and reliability?
3. What are the four route tiers?

<details><summary>Answers</summary>

1. No liquidity = the payment physically can't execute. Impossible paths are eliminated before scoring, not scored and ranked low.
2. They stay in the equation with lower weights (5% cost, 35% reliability). They never zero out — a high-failure route still loses.
3. Optimal, admissible, fallback, eliminated.
</details>

---

## Day 6 — Pareto and constraints

> 📖 **Read first:** HTML → *Part II — Chapter 4* · PDF pp. 22–24
> 🗂 **Repo:** none

### The one idea
> Aiva has **contradictory objectives** — fastest vs cheapest vs safest. You can't average them. You optimise them as a constrained problem.

### ⚙️ MECHANISM #4 — What "dominated" really means

> **Not:** "every other route surpasses it."
> **But:** A route is dominated when **at least one** other route beats it on **every** dimension.

Three paths:

- **P1** — fast, higher risk → on the frontier
- **P2** — slower, lower risk → on the frontier
- **P3** — slower than P1 **and** riskier than P2 → **dominated**

P1 and P2 both survive because each wins at something. Neither dominates the other — choosing between them requires a **tradeoff**. P3 wins at nothing, so it can never be correct no matter what you're optimising for.

> **Routes on the Pareto frontier require tradeoffs. Dominated routes don't — they're just worse.**

In V0 terms: Fast Route = P1, Balanced Route = P2. High urgency weights toward P1, normal weights toward P2.

### ⚙️ MECHANISM #8 — Hard vs soft constraints

> **Not:** "corridors get eliminated or scores get lowered."
> **But:** the *consequence* of getting it wrong is what matters.
>
> - **All-hard** → almost every corridor gets eliminated by one minor issue. You end up with **no feasible options**.
> - **All-soft** → Aiva might select a corridor that **literally cannot execute** — a failed sanctions screen just becomes a low score, and it still gets picked.
>
> The distinction is **safety vs flexibility**: hard constraints prevent impossible routes from ever being selected; soft constraints keep good routes usable despite minor imperfections.

| Hard (violate → eliminated) | Soft (violate → penalised) |
|---|---|
| Sanctions conflict | Slightly higher hop latency |
| Reliability below threshold | Slightly worse FX spread |
| Liquidity below minimum | Moderate volatility |
| RTGS window incompatible | Moderate compliance friction |
| Regulatory blocker | Extra hop required |

### The optimisation pipeline

```
All corridors → HARD FILTER → Feasible set → SOFT PENALTIES → Utility optimisation → Optimal route
```

Formally: **maximise U(route) subject to H(route) = 0**

Volatility across a multi-hop route sums as **σ_total = Σ(σᵢ × √tᵢ)** — a 3-hop corridor has three exposure calculations added together. Breach the cap and the whole corridor is eliminated.

### 🎤 Say it like this
> "A route only survives if nothing beats it on every dimension. Everything else is dominated and never selected. Then hard constraints eliminate the impossible, soft constraints penalise the imperfect, and the utility function picks the winner from what's left."

### ✅ Check yourself
1. What makes a route "dominated"?
2. What goes wrong if every constraint is hard? If every one is soft?
3. Why do P1 and P2 both survive when one is slower?

<details><summary>Answers</summary>

1. At least one other route beats it on **every** dimension — so it can never be right regardless of weighting.
2. All-hard: one minor issue kills good routes, you end up with nothing feasible. All-soft: Aiva can select corridors that physically can't execute.
3. Neither beats the other on everything — P1 wins on speed, P2 on risk. Choosing requires a tradeoff, which is what the Pareto frontier is.
</details>

---

## Day 7 — Consolidation (no new material)

> 📖 **Read:** re-skim whichever two sessions felt weakest
> 🗂 **Repo:** none

### Do this, in order

**1. Draw it from memory.** Blank page. Draw: request → Aiva (7 graphs → utility → Pareto) → blueprint → Rail → Cloked. No notes. Then check against Days 4–6.

**2. Say the twelve-minute version out loud.** Record it on your phone. Cover: the legacy problem, why messaging matters, corridors and σ√t, the seven graphs, scoring and weight shifts, Pareto and constraints. Play it back — anywhere you hear yourself say "kind of" or "sort of", that's a gap.

**3. Re-answer all six mechanisms from this week** without scrolling: #1 (SWIFT), #2 (σ√t), #3 (simultaneous), #4 (dominated), #5 (deterministic), #6 (liquidity gatekeeper), #7 (weights), #8 (hard/soft).

**4. The pitch chain.** String these five sentences into one flowing answer:

> Legacy is reactive; Lupine is predictive. → SWIFT moves messages, not money; nothing in the chain decides if the route was right. → The real FX rate is eight components, and delay itself is one of them. → Aiva evaluates seven dimensions simultaneously and outputs a deterministic blueprint. → Same inputs, same route, every time — knowable before the money moves.

If you can say that unbroken, Week 1 is done.

---

# WEEK 2 — EXECUTION, EVIDENCE, YOUR SYSTEM, THE MARKET

---

## Day 8 — RAIL: making it actually happen

> 📖 **Read first:** HTML → *Part III — Chapters 2 + 3* · PDF pp. 25–27
> 🗂 **Repo:** [**R4 — Rail**](#r4--rail-day-8-10-min) *(10 min)*

### The one idea
> Aiva decides. **Rail is where things actually break** — and it's built so that breaking never leaves money stuck.

### The hop state machine

Full model: **Init → Precheck → Execute → Observe → Confirmed → Committed → Final**

Your V0's simpler version: **initiated → scored → route_selected → executing → completed** (or **failed**)

The critical property: **there are no ambiguous states, ever.** A payment is always in exactly one known state.

### ⚙️ MECHANISM #10 — Atomicity *(the one you couldn't answer in April)*

> **Atomicity = a hop either commits fully, or the system compensates. There is nothing in between.** No half-settled corridors. No partial transfers.

Why enforced transitions *are* atomicity in code: **each state becomes a promise.** By the time a payment reaches `completed`, every prior state has been visited and logged — guaranteed.

If arbitrary jumps were allowed, you could mark a payment `completed` without ever running execution. That's a **ledger lie** — a record claiming something happened that didn't. Your V0 raises an error on any invalid transition, which makes that lie structurally impossible.

> **Enforced transitions don't just organise the code — they make the audit trail trustworthy.**

### Idempotency

> **IdempotencyKey = SHA256(payment_id + hop_id + sequence_id)**

Send the same instruction twice and the second one is recognised and ignored. Prevents double-settlement, double-custody, and replay attacks.

### Smart retries

> **Retry(n) = BaseDelay × (GrowthFactor^n)**, with GrowthFactor < 2

Not just "try again" — retries include adaptive risk escalation (tighter thresholds), time-window sensitivity (defer to the next RTGS window), and liquidity feedback.

### ⚙️ MECHANISM #9 — Forward correction, not rollback

> **Not:** "it'd be a payment gateway in itself."
> **But:** Inside one bank, rollback is trivial — reverse a ledger entry, they control both sides. **Across borders, once money leaves an institution, that institution no longer controls it.** A "rollback" becomes an entirely new payment going the other way — subject to every single failure mode the first one had.
>
> So Lupine never reverses. Aiva pre-computes a **fallback tree**, so when hop 3 fails, **hop 3b is already ready**. The payment completes **forward** through a different final path.

```
Legacy:  Hop1 → Hop2 → Hop3 ✗ … money stuck in limbo
Lupine:  Hop1 → Hop2 → Hop3 ✗
                     ↘ Hop3b → Hop4 ✓  (pre-computed by Aiva)
```

### 🎤 Say it like this
> "Legacy systems try to roll back failed payments, which turns one stuck payment into two stuck payments. We pre-compute fallbacks so money always completes forward. And every payment moves through a strict state machine — you can't skip steps, can't be in two states at once, every transition is logged. That's what deterministic looks like at the execution layer."

### ✅ Check yourself
1. What does atomicity mean, and how do enforced transitions deliver it?
2. Why is rollback fundamentally harder across borders than inside one bank?
3. What is idempotency preventing?

<details><summary>Answers</summary>

1. Commit fully or compensate — never in between. Enforced transitions make each state a promise: reaching `completed` guarantees every prior state was visited and logged, so you can't fake a success.
2. Inside a bank, it's a ledger reversal — they control both sides. Across borders, once money leaves, that institution doesn't control it; rollback becomes a fresh payment with all the same risks.
3. Double-settlement, double-custody, replay attacks — duplicate instructions get recognised and ignored.
</details>

---

## Day 9 — CLOKED: proving it happened

> 📖 **Read first:** HTML → *Part IV — Chapters 1 + 4* · PDF pp. 28–30
> 🗂 **Repo:** [**R5 — Cloked**](#r5--cloked-day-9-10-min) *(10 min)*

### The one idea
> Aiva proves **why**. Rail proves **how**. Cloked proves **that it actually happened** — without anyone having to trust you.

### The problem

Banks and hospitals rely on logs that can be **edited, deleted, or fabricated**. SQL tables, S3 buckets, PDFs, handwritten slips. None of it is cryptographically accountable.

### Two layers of linking

**Layer 1 — hash chain inside one Evidence Capsule.** Every event in a single payment gets hashed and linked to the one before it:

> **H(Eₙ) = SHA256(Eₙ + H(Eₙ₋₁))**

**Layer 2 — ledger blocks linking capsules across time.** Each completed payment produces a capsule; capsules get wrapped in blocks chained to each other. *A chain inside a chain* — the capsule chain proves one payment was honest, the ledger chain proves the whole history is intact.

**Anchoring** — periodic external checkpoints to regulators (AUSTRAC, MAS, EMA).

### ⚙️ MECHANISM #11 — Exactly how tampering is caught

> **Not:** "any break in the chain means it's been tampered with."
> **But:** here is the actual attack, step by step —
>
> 1. Attacker edits **entry #2**.
> 2. `verify_chain()` recomputes #2's hash from its own data. It no longer matches the stored hash. **Caught.**
> 3. So the attacker also updates #2's stored hash to match. Now #2 looks clean —
> 4. — but **#3's `previous_hash` still points at the OLD hash of #2**. The link is broken. **Caught.**
> 5. To fix that, they must rewrite #3. Which breaks #4. Which breaks #5…
>
> **One tampered entry forces rewriting every entry after it, all the way to the end.** Single-point edits are mathematically impossible.

That step-by-step is what makes the demo land. "It breaks" is a claim; the walkthrough is a proof.

### ⚙️ MECHANISM #12 — Verifiable vs verbal trust

> **Not:** "trust should be verified and displayed."
> **But:**
> - **Verbal trust** = "we say it happened this way, here are our logs." You must trust the sender's word, their database, their compliance team.
> - **Verifiable trust** = "here's the evidence — **you can verify it mathematically without trusting me at all.**" The recipient runs the verification themselves. Even if the company vanished, the proof still holds.
>
> **You don't need to trust the source. The math does the trusting for you.**

For A$500K to Singapore that means: prove to your auditor the right route was chosen, prove to MAS/AUSTRAC compliance ran at every hop, prove the payment moved exactly as claimed. **None of that is possible with bank logs today.**

### Why Cloked is not a blockchain

Regulated industries **can't** use public blockchains — evidence must be private, latency must be low, and there's no need for decentralised consensus. Cloked takes the good parts (cryptographic linking, append-only, tamper-evident) without the baggage (public ledger, consensus latency, gas fees).

### Audit replayability

Given any block, a regulator can retrieve the capsule, recompute the chain, verify the parent hash, replay the execution, rebuild the route matrix, and re-evaluate compliance. Not *"we have logs"* — **"we can prove."**

### 🎤 Say it like this
> "Banks ask you to trust their records. We give you records you can verify mathematically. Tamper with any payment record and the chain breaks at exactly that point and every record after it — you can't edit one entry, you'd have to rewrite history."

### ✅ Check yourself
1. Walk through tampering with entry #2, step by step.
2. What's the difference between verbal and verifiable trust?
3. Why isn't Cloked a blockchain?

<details><summary>Answers</summary>

1. Edit #2 → recomputed hash mismatches → fix #2's hash → but #3's `previous_hash` still references the old one → must rewrite #3, then #4, then everything after. Single edits are impossible.
2. Verbal: trust my logs. Verifiable: verify it yourself without trusting me — the proof holds even if I disappear.
3. Evidence must be private, latency must be low, no need for decentralised consensus. Cloked keeps the cryptographic linking without the public-ledger baggage.
</details>

---

## Day 10 — Your system: what's real and what isn't

> 📖 **Read:** none — this is about your own system
> 🗂 **Repo:** none, but this day *is* repo-adjacent. R1–R5 should make it click.

### The one idea
> The fastest way to lose a room is to overclaim and get caught. **Know your edges better than anyone questioning you.**

### Genuinely real and running right now

| | |
|---|---|
| **Live FX** | Four independent sources with automatic fallback |
| **Scoring engine** | Real math, fully deterministic |
| **Urgency weighting** | Four profiles, working |
| **Evidence chain** | Real SHA-256, real tamper detection |
| **State machine** | Enforces every transition |
| **Watcher agent** | 720+ hourly runs, live signals, opens GitHub Issues on STRIKE |
| **90-day backtest** | Real historical ECB rates, replayed through the engine |
| **21 rails** | Modelled from published fee schedules |
| **Public site** | Deployed, auto-updating daily, self-healing |

### Simulated or not yet built — say these without flinching

- **No money moves.** Execution is simulated end to end.
- Provider fees are **modelled from published rates**, not live API quotes.
- **Rail never fails** — no retry, failover, or forward correction implemented.
- **No persistence** in the API — the evidence log doesn't survive a restart.
- No hard-constraint filter. No compliance layer.
- No Layer-2 ledger blocks, no external anchoring.
- **One corridor only**: AUD→SGD.

### The three questions that will catch you

**"You claim Pareto frontier selection but it's just a weighted sum."**
> "A weighted-sum maximiser always lands **on** the Pareto frontier, so selection is sound. What we haven't built is explicit dominance **filtering** and the admissible/fallback/eliminated tiering — that's P2-Ch2, and it's on the roadmap."

**"Are these real quotes?"**
> "They're modelled from published fee schedules — Wise's public calculator, Airwallex and Nium business pricing, ANZ and CBA SWIFT schedules. The FX rate is genuinely live. Live provider quotes are the next integration."

**"So nothing actually moves money?"**
> "Correct — V0 is the decision and evidence layer. Execution is simulated. That's deliberate: it means we don't need a remittance licence to prove the intelligence works, and the intelligence is the hard part."

**Every one of those answers is stronger than a bluff.** Knowing your gaps precisely reads as competence. Vagueness reads as not understanding your own system.

### ✅ Check yourself
1. Name five things that are genuinely live.
2. Name five things that are simulated.
3. Answer the Pareto challenge out loud.

---

## Day 11 — Your system as a demo

> 📖 **Read:** none
> 🗂 **Repo:** [**R6 — The live system**](#r6--the-live-system-day-11-20-min) *(20 min)*

### The one idea
> You're not showing software. You're showing **a decision being made, and proved.**

### The narrative arc

**1. Set the stakes.** *"A$500,000, Australia to Singapore. Through a bank that's 250 basis points — A$12,500 — and a day and a half of not knowing where it is."*

**2. Show the decision.** Open the site, run a transfer. Twenty-one rails scored simultaneously, one winner, with a written rationale.

**3. Change urgency — this is the moment.** Switch normal → critical. **The winner changes.** Narrate it: *"Same rails, same rate, same instant. What changed is what we're optimising for. Speed went from 25% to 60% of the decision. Reliability stayed at 35% — it never switches off."*

**4. Show the evidence chain.** Four hashed entries, each linked to the last, `chain_valid: true`. *"If anyone edits any of these, the chain breaks there and at every entry after it."*

**5. Show the watcher.** *"This has been running hourly for months without me. Right now it's saying the rate is in the Xth percentile of the last 60 days. It opens a GitHub issue on its own when the corridor hits the top decile."*

**6. Land the thesis.** *"Legacy is reactive. This is predictive, deterministic, and provable."*

### The numbers to have memorised

- **A$500,000** — the reference transfer
- **~45 bps** — Wise, the usual winner at normal urgency
- **~250 bps** — generic bank SWIFT, the baseline
- **~A$10,270** — saved per transfer vs bank SWIFT
- **21** — rails compared
- **4** — urgency profiles
- **60 days** — the watcher's lookback window
- **Top 10%** — the STRIKE threshold

### ✅ Check yourself
1. Deliver the six-step demo out loud, timed. Aim for under four minutes.
2. Explain from memory why the winner changes at critical urgency.

---

## Day 12 — Wise: the operator who built their own rails

> 📖 **Read first:** HTML → Wise: *Our Infrastructure* · *Pricing philosophy + take rate economics* · *CEO letter* · PDF pp. 32–42
> 🗂 **Repo:** [**R7 — Automation**](#r7--automation-day-12-15-min) *(15 min)*

### Why this matters
Wise is the real-world proof that corridor engineering works commercially — **and the clearest evidence of what you're *not* doing.** The study pack puts it exactly right: Wise is the **architectural opposite** of Lupine. They *exit* the correspondent rails entirely. You *route across* them.

### What they built

They replaced correspondent banking by **"stitching together local payment systems, eliminating intermediaries."** Four elements: expansions/integrations, technology, regulatory, operations.

**The scale:**

| | |
|---|---|
| Licences | 63, across 12 countries |
| FX routes | 2,500+ |
| Local processing | 88 countries, 85 local FI partnerships |
| Engineers | 500+, ~90 production deploys **per day** |
| Volume | £5bn/month; £1bn saved for customers annually |
| Uptime | 99.9%, with 5× headroom |

**The integration payoff — memorise these two:**
- **UK FPS**: partner bank fees cut **nine-fold**, transfers under **20 seconds**
- **Hungary (MNB)**: prices dropped **14%**, instant transfers went from **17% → 82%**
- **Singapore**: directly connected to **FAST**

**Treasury intelligence:** a proprietary global treasury system does real-time liquidity prediction and smart fund routing. **~50% of traded volumes are predicted by ML** — which is what lets them run on low working capital.

### The take rate (know these numbers)

| | FY2021 | FY2020 | FY2019 |
|---|---:|---:|---:|
| Total take rate | 0.77% | 0.73% | 0.66% |
| Cross-currency | 0.70% | 0.68% | 0.64% |
| Other fees | 0.07% | 0.05% | 0.02% |

**0.70% ≈ 70 bps.** That's the market's honest all-in price for cross-border FX at consumer scale — and it's the number your 45 bps Wise model sits under because you're modelling large-transfer business pricing, not retail.

### The positioning line

Wise built **rails**. Ten years, 63 licences, 500 engineers. You are **not** competing with that — and shouldn't try.

> "Wise spent ten years and 63 licences building rails. We're not rebuilding those rails — we're building the intelligence layer that decides **which** rails to use, and proves the choice. Wise is one of the twenty-one options our engine scores."

That reframe turns your biggest apparent weakness (you have no rails) into your actual position (you're rail-agnostic, which Wise can never be).

### ✅ Check yourself
1. What was Wise's FY2021 cross-currency take rate, and what does it represent?
2. What happened when Wise integrated with UK FPS?
3. Why aren't you competing with Wise?

<details><summary>Answers</summary>

1. 0.70% (~70 bps) — the market's real all-in price for cross-border FX at consumer scale.
2. Partner bank fees fell nine-fold; transfers dropped to under 20 seconds; prices to customers fell.
3. They built rails over ten years with 63 licences. You build the intelligence layer that chooses between rails — including theirs. Rail-agnostic beats rail-owning for routing decisions.
</details>

---

## Day 13 — Adyen and Remitly: platform and network

> 📖 **Read first:** HTML → Adyen: *The payments value chain* · *One single platform* · *RevenueAccelerate* · *Key benefits — failover + double-entry* · *Six data centres* · PDF pp. 42–61
> HTML → Remitly: *Global network + treasury* · *Technology platform deep-dive* · *Hybrid risk model* · PDF pp. 63–78
> 🗂 **Repo:** none

**Today is the most important market day.** Three of these sections show your architecture **already running in production at someone else's company** — which is simultaneously validation and a competitive warning. Read the "Why read" notes in the HTML carefully; they make the links explicit.

### ⚠️ The three that should make you sit up

| Reading | What it actually is |
|---|---|
| **Adyen — Key benefits + Six data centres** | Six live data centres across continents, **"traffic can be rerouted real-time whenever needed."** That is your **forward-correction** concept (P3-Ch2+3) — in production **since 2018**. Their **double-entry accounting core** is the production big sibling of Cloked. |
| **Adyen — RevenueAccelerate** | ML that **modifies each payment request in real time** to target the highest approval probability. This is the closest live analogue to Aiva's scoring engine. |
| **Remitly — Technology platform** | The study pack flags a **"Perfect Delivery Promise"** — deterministic settlement prediction **sold as a customer-facing feature**. Someone is already commercialising the word you want to own. |

**Don't panic about this — use it.** The correct read isn't "I've been beaten." It's: *deterministic delivery is provably commercially valuable, three companies have built pieces of it inside their own walls, and none of them can do it across providers or prove it cryptographically.* That's a much stronger pitch than pretending you invented the idea.

### Adyen — the single platform thesis

The card payments value chain has five core parties: **shopper → merchant → acquirer → card network → issuer**, plus terminal/gateway providers, processors, and risk-management providers bolted on over time.

The problem: merchants had to stitch together a **disparate group** of gateways, risk providers, processors and acquirers — each a separate integration, separate contract, separate failure point.

**Adyen's move:** one integrated platform spanning the **entire** value chain. (For scale: the six largest card networks moved **$23.0 trillion** in purchase volume in 2017.)

**The lesson for Lupine:** the winning play in payments has repeatedly been **collapsing a fragmented chain into one coherent layer**. Adyen did it for card acceptance. You're proposing it for cross-border routing intelligence — replacing "every bank decides in isolation" with one engine that sees the whole path.

### Remitly — corridors at scale, and the data flywheel

| | |
|---|---|
| Corridors | **1,700+** |
| Reach | 17 send countries → 115+ receive, 75+ currencies |
| Partners | 15+ top-tier banks; **100 direct integrations** |
| Disbursement | 3.5bn bank accounts, 630m mobile wallets, 355k cash pickup points |
| Speed | **>75% of transactions complete in under one hour** |

**Their four advantages:** global reach, local expertise, **control over the transaction lifecycle** (direct integrations let them optimise routing for cost, risk and compliance), and AI/ML-driven fraud and risk management.

**The flywheel:** more customers → more transactions → more data → better marketing, experience and pricing → more customers. Ten years of transaction data as a compounding asset.

**Their pricing and treasury are linked:** a proprietary pricing engine uses ML to find pricing levers per corridor, tied to a treasury program with **currency-level forecasting algorithms** to predict demand and optimise trading.

### The compliance gap this fills

Remitly's risk architecture is **hybrid**: ML models + early-warning systems + bespoke rules + manual investigation, tuned to keep fraud losses "within desired guardrails."

That matters because **your V0 skipped the compliance graph entirely** (it's 1 of the 2 graphs out of scope). When someone asks *"where's your compliance layer?"*, the honest, informed answer is:

> "Out of V0 scope deliberately. And production compliance isn't one model — Remitly's own filings describe a hybrid of ML, early-warning systems, bespoke rules and manual investigation. That's the shape we'd build toward, not a single classifier."

### Where Lupine sits

- **Wise** owns **rails** — and exited correspondent banking to get them.
- **Remitly** owns a **corridor network** and a compounding data flywheel.
- **Adyen** collapsed a **fragmented value chain** into one platform, with real-time failover.
- **Lupine** owns the **decision and evidence layer** — rail-agnostic, provider-agnostic, and the only one producing a cryptographic proof of *why* a route was chosen.

> "Wise, Adyen and Remitly all optimise routing **inside their own network** — and they're genuinely good at it. But none of them can tell you whether a **competitor's** rail would have been better for your payment, because that's against their interest. And none of them hand you a proof you can verify without trusting them. We're rail-agnostic and we're provable. That's the gap."

**Why this positioning is defensible:** their optimisation is structurally captive. Wise can't recommend Airwallex. Adyen can't route you off Adyen. The neutrality *is* the product — and it's the one thing an incumbent can't copy without cannibalising itself.

### ✅ Check yourself
1. What did Adyen collapse, and what's the parallel for Lupine?
2. What is Remitly's flywheel?
3. Adyen has had real-time rerouting since 2018. Why isn't that fatal to you?
4. In one sentence, where does Lupine sit relative to all three?

<details><summary>Answers</summary>

1. A fragmented card value chain (gateways, processors, acquirers, risk providers) into one platform. Lupine collapses fragmented, isolated routing decisions into one intelligence layer.
2. More customers → more transactions → more data → better pricing/marketing/experience → more customers. Ten years of transaction data compounding.
3. Their rerouting happens **within Adyen's own infrastructure** — between their own data centres, for their own traffic. It proves the architecture works; it doesn't cover choosing between independent providers, and it produces no verifiable evidence for the payer.
4. They optimise routing within their own networks; Lupine is the rail-agnostic decision and evidence layer that scores across all of them and proves the choice.
</details>

---

## Day 14 — Cold exam

**No notes. Say everything out loud. Record it.**

### Part 1 — The twelve mechanisms (2 min each)

State the precise version of each:

1. What does SWIFT actually do?
2. What does the √ in σ√t mean for route selection?
3. Why is simultaneous evaluation better than sequential?
4. What makes a route dominated?
5. Define deterministic.
6. Why is liquidity a gatekeeper?
7. At critical urgency, what happens to cost and reliability?
8. What breaks if all constraints are hard? If all are soft?
9. Why is rollback impossible across borders?
10. What is atomicity, and how do enforced transitions deliver it?
11. Walk through tampering with entry #2.
12. Verbal vs verifiable trust?

### Part 2 — End to end (5 min, unbroken)

Trace **A$500,000, AUD→SGD, critical urgency** from request to proof. Cover: what Aiva does, which weights apply and why, how the winner is selected, what the blueprint contains, how Rail executes it, what atomicity guarantees, and what Cloked produces.

### Part 3 — Hostile questions (answer immediately, no hedging)

- "Isn't this just a comparison site?"
- "Wise already does routing. Why do you exist?"
- "You claim Pareto but it's a weighted sum."
- "Nothing actually moves money — so what have you built?"
- "What stops a bank building this in six months?"
- "Why should anyone trust your evidence chain?"

### Part 4 — The 60-second pitch

Legacy is reactive → the intelligence gap → what Aiva/Rail/Cloked do → what's live today → what's next.

### You're done when

You can deliver Part 2 unbroken, and every Part 3 answer names a real limitation without sounding defensive.

### Repo questions (add these to Part 3)

- Where do the urgency weights live, and what would you change to make critical urgency weight speed at 70%?
- Which file would you change to add a 22nd provider?
- Your API loses all evidence on restart. Which file, and why does it matter?
- The site says data is fresh daily. What actually makes that happen?

---

# THE REPO TRACK — 7 sessions

**The goal is literacy, not fluency.** You are not learning to write Python. You are learning the floor plan — so you can direct changes precisely, debug conversationally, and explain your own system to a technical person without hand-waving.

**How to look at a file:** open it on GitHub in your browser. **Read the comments and the names, skip the logic.** Names like `WEIGHT_PROFILES`, `valid_transitions`, `verify_chain` tell you nearly everything. If a block looks like maths, skim past it — you'll know *what it does* from the surrounding names, and that's enough.

### The whole repo in one view

```
lupine-systems-core/
│
├── src/                          THE ENGINE (1,003 lines)
│   ├── models/schemas.py           the nouns — every object in the system
│   ├── aiva_lite/                  🧠 LAYER 1 — decide
│   │   ├── router.py                 the catalogue: 21 rails
│   │   ├── scorer.py                 the judge: weights + composite score
│   │   └── selector.py               the spokesperson: winner + rationale
│   ├── rail_lite/executor.py       🚂 LAYER 2 — execute (state machine)
│   ├── cloked_lite/logger.py       🔒 LAYER 3 — prove (hash chain)
│   ├── data/fx_feed.py             live FX, 4-source fallback
│   └── api/main.py                 the 5 endpoints
│
├── scripts/                      THE LIVE SYSTEM (743 lines)
│   ├── watcher.py                  hourly market agent
│   ├── backtest.py                 90-day replay
│   ├── generate_live_decisions.py  daily decisions → JSON
│   ├── generate_site_data.py       news + health + backtest dispatch
│   └── fetch_daily_news.py         daily news scan
│
├── website/                      THE SHOP WINDOW
│   ├── index.html                  the whole site (engine mirrored in JS)
│   └── data/*.json                 5 files the site reads
│
├── tests/                        4 files, 10 deterministic tests
├── .github/workflows/            4 workflows — the automation
├── docs/                         study pack, guide, spec, this handbook
├── daily-news/  test-results/    one .md per day, auto-generated
└── CLAUDE.md                     the brief every AI agent reads first
```

**The single most important thing on this page:** the folder names `aiva_lite`, `rail_lite`, `cloked_lite` are the three layers from the book, one folder each. **The architecture is visible in the file tree.** That's not an accident, and it's worth saying out loud in a technical conversation.

---

### R1 — The map *(Day 2, 15 min)*

**Look at:** the repository root on GitHub. Just the folder list. Then open `CLAUDE.md`.

**The one thing to understand:** every folder has exactly one job, and the three-layer boundary is enforced by the structure. Aiva decides, Rail executes, Cloked proves — and no folder reaches into another's job.

**Do this:**
1. Open the repo root. Match each folder to the tree above.
2. Open `CLAUDE.md` and read Sections 2 and 3. This is the file every AI agent reads before touching your code — it's why changes stay consistent.
3. Note `src/` (the engine, reusable) vs `scripts/` (jobs that run on a schedule). Scripts *call* the engine; the engine never calls a script.

**✅ Check:** Name the three layer folders and what each does. Where does live FX live — `src/` or `scripts/`? *(Answer: `src/data/` — it's engine, not a job.)*

---

### R2 — The data foundation *(Day 3, 15 min)*

**Look at:** `src/models/schemas.py` (77 lines) · `src/data/fx_feed.py` (116 lines) · `website/data/`

**The one thing to understand:** `schemas.py` defines every **noun** in the system. Nothing exists that isn't defined here.

| Object | What it is |
|---|---|
| `MovementRequest` | what you want to move — amount, currencies, urgency |
| `RouteOption` | one candidate rail — time, cost, reliability, plus scores once judged |
| `DecisionScore` | the verdict — winner, rationale, weights used |
| `ExecutionState` | where the payment is in the state machine + full history |
| `EvidenceEntry` / `EvidenceLog` | one sealed record / the whole chain |

`fx_feed.py` is Day 3's concept in code: four source functions tried in order, first success wins. You can literally see the fallback chain as a list.

**Do this:** open `schemas.py` and read only the field names. Then open `fx_feed.py` and find `_SOURCES` — that one line *is* the fallback chain.

**✅ Check:** Which object holds the rationale text a user reads? What happens if source #1 is down? *(Answers: `DecisionScore`. It silently falls through to source #2 — the system never notices.)*

---

### R3 — Aiva *(Day 5, 20 min)*

**The best pairing in the course** — you'll have just learned scoring, and `scorer.py` is 41 lines.

**Look at:** `src/aiva_lite/router.py` · `scorer.py` · `selector.py`

| File | Role | The thing to find |
|---|---|---|
| `router.py` | **the catalogue** | the 21 providers, each with hours / bps / reliability |
| `scorer.py` | **the judge** | `WEIGHT_PROFILES` — your four urgency profiles, exactly as in Day 5 |
| `selector.py` | **the spokesperson** | the sentence template that writes the human rationale |

**Two things worth knowing:**

**1. The `fx_rate` switch.** `generate_routes()` behaves differently depending on one input: give it a live rate → 21 real providers; leave it out → 3 simulated routes (Fast / Cheap / Balanced). The tests use the 3-route path because fixed numbers make assertions possible. **Both paths are real code; one is for testing.**

**2. Where the Pareto gap lives.** `selector.py` takes the highest-scoring route. It does **not** compute a dominance frontier or classify admissible/fallback/eliminated. That's the honest limitation from Day 10 — and now you know it's a ~44-line file, so you know it's a small fix, not a rewrite.

**✅ Check:** Which file holds the weights table? Which writes the "Beat Balanced Route by 0.059…" sentence? What changes when `fx_rate` is supplied?

---

### R4 — Rail *(Day 8, 10 min)*

**Look at:** `src/rail_lite/executor.py` (62 lines — the whole execution layer)

**The one thing to understand:** find `valid_transitions`. It's a short list saying *from this state, you may only go to these states.* **That list is Day 8's atomicity principle, in code.** Anything not on it raises an error.

Three functions: `create_execution` (start), `advance_state` (move one step, enforce the rule), `simulate_full_execution` (run the whole sequence).

**Where the limitation lives:** `simulate_full_execution` always reaches `completed`. There's no failure branch, no retry, no fallback. That's the "Rail never fails" gap from Day 10 — and it's why `failed` exists as a state but is never used.

**✅ Check:** What stops a payment jumping straight from `initiated` to `completed`? Why does that matter for the audit trail? *(Because reaching `completed` guarantees every prior state was visited and logged — you can't fake a success.)*

---

### R5 — Cloked *(Day 9, 10 min)*

**Look at:** `src/cloked_lite/logger.py` (63 lines — the entire evidence layer)

**The one thing to understand:** three functions, and the whole trust story lives in them.

| Function | What it does |
|---|---|
| `create_evidence_log` | start a new chain for one payment |
| `append_evidence` | hash this event **together with the previous hash**, add it |
| `verify_chain` | walk every entry, recompute each hash, check every link |

Find the word `"genesis"`. That's the placeholder for entry #0's "previous hash" — the chain's anchor point. Everything after links backward to it.

`verify_chain` is the file's most important eight lines: for each entry it checks (a) does the recomputed hash match the stored one, and (b) does `previous_hash` match the entry before. **Those two checks are exactly the two-step tamper detection from Day 9.**

**✅ Check:** Which function makes tampering detectable, and what two things does it check?

---

### R6 — The live system *(Day 11, 20 min)*

**Look at:** `scripts/` · `website/data/` · `src/api/main.py`

**The one thing to understand:** the engine in `src/` doesn't do anything on its own. The scripts are the **jobs that call it on a schedule** and write results to JSON that the website reads.

| Script | Runs | Produces |
|---|---|---|
| `watcher.py` | hourly | `agent_signal.json` — STRIKE / WATCH / HOLD |
| `generate_live_decisions.py` | daily | `live_decisions.json` — all 4 urgency levels |
| `backtest.py` | daily | `backtest.json` — 90-day replay |
| `fetch_daily_news.py` | daily | `daily-news/YYYY-MM-DD.md` |
| `generate_site_data.py` | daily | `news.json`, `health.json`, triggers backtest |

**The website reads five JSON files.** That's it — no server, no database. That's why the site is fast and free to host.

**⚠️ The one duplication you must know about.** `website/index.html` contains `TR_PROVIDERS` — a JavaScript copy of the same 21 providers that live in `router.py`. They're kept in sync **by hand**. Change a fee in one and the other is silently wrong. If anyone technical reviews your repo, they will spot this — so name it before they do.

`src/api/main.py` holds the 5 endpoints. Note: it stores everything in memory, so evidence dies on restart. The scripts don't use the API at all — they call the engine directly.

**✅ Check:** Where does the website get its numbers? What breaks if you change a provider fee in only one place?

---

### R7 — Automation *(Day 12, 15 min)*

**Look at:** `.github/workflows/` — four files

| Workflow | Trigger | Job |
|---|---|---|
| `ci.yml` | every push | run the tests |
| `daily.yml` | hourly + 08:00 UTC | tests → news → decisions → site data → commit |
| `watcher.yml` | every hour at :30 | run the watcher, open an Issue on STRIKE |
| `pages.yml` | every push to main | deploy the website |

**The one thing to understand — the self-healing design.** `daily.yml` fires **24 times a day** but skips instantly if today's work is already done. GitHub would have to drop all 24 slots to miss a day. Combined with `continue-on-error` on every step and `git pull --rebase` before every commit, the pipeline survives network blips and two jobs pushing at once.

**This is a genuinely good story to tell.** *"It's been running unattended for months — 720+ watcher runs, zero manual intervention. The pipeline heals itself."* That's an engineering-maturity signal most pre-seed demos can't offer.

**✅ Check:** Why does the daily job run 24 times instead of once? What are the two safeguards that stop concurrent jobs breaking each other?

---

## 🔧 How to direct changes

**The most practically useful table in this document.** When you want something changed, this is what to tell me:

| You want… | It's in | Say to me |
|---|---|---|
| Different urgency weights | `scorer.py` | *"Change critical urgency to 70% speed"* |
| Add / edit / remove a provider | `router.py` **and** `index.html` | *"Add Payoneer at 60 bps, 24h, 0.89 — both places"* |
| Different reference amount | `scripts/*.py` | *"Change the reference transfer from 500K to 250K"* |
| A new corridor (e.g. AUD→USD) | `scripts/` + `router.py` | *"Add AUD→USD as a second corridor"* |
| Change the STRIKE threshold | `watcher.py` | *"Make STRIKE fire at top 5% instead of top 10%"* |
| Change how the rationale reads | `selector.py` | *"Make the rationale mention dollar savings"* |
| Anything visual on the site | `website/index.html` | *"Make the provider cards show a savings badge"* |
| Add a new logged event | `logger.py` + caller | *"Log an fx_source event in the chain"* |
| Change how often something runs | `.github/workflows/` | *"Run the watcher every 30 minutes"* |
| Real failure simulation in Rail | `executor.py` | *"Make execution fail based on reliability score"* |
| Persist evidence across restarts | `api/main.py` | *"Add a database so evidence survives restart"* |
| Pareto dominance filtering | `selector.py` | *"Add explicit dominance filtering and route tiers"* |

Knowing which file to name is the whole difference between *"can you make it better"* and directing an engineer. **That's what repo mastery means for you.**

---

## The whole thing on one page

**The problem.** Cross-border payments hop through correspondent banks with mismatched hours, liquidity, and compliance. Same payment: 2.5 hours or 11 days. Nobody can tell you which, or why.

**The gap.** SWIFT carries instructions but decides nothing. gpi shows you problems after they happen. No layer predicts.

**Aiva** — evaluates seven dimensions simultaneously, scores every corridor with a weighted utility function, eliminates the impossible with hard constraints, penalises the imperfect with soft ones, and selects from the Pareto frontier. Weights shift with urgency; nothing ever switches off. Output: a deterministic blueprint.

**Rail** — executes the blueprint through a strict state machine. No ambiguous states, no skipped steps. Atomicity: commit fully or compensate. Idempotency stops double-settlement. Failures go **forward** through pre-computed fallbacks, never backward.

**Cloked** — hashes every event into a chain where each entry links to the last. Tamper with one and you must rewrite all of them. Verifiable trust: the recipient proves it themselves without trusting you.

**One sentence:** *Lupine makes cross-border payments deterministic — the route is computed, not guessed; the execution can't skip a step; and the whole decision is provable by anyone, without trusting us.*
