# CLAUDE.md — Lupine

> Canonical context for AI coding agents in this repo.
> **The code in `src/` is ground truth.** This file says what the project is for, how to work with
> its owner, and what the code really does. Full module-by-module detail: `docs/architecture.md`.

---

## 1. Direction (active since 16 October 2026)

Lupine is the project through which **Chris (Chirantan Gogoi), in Hobart**, learns and builds
toward an **energy infrastructure technology company, starting in Tasmania**. The repository
supports three connected activities:

1. **Developing technical understanding**: electrical, computing and software foundations.
2. **Conducting reproducible engineering experiments**: low-voltage, safe, documented.
3. **Discovering a worthwhile product**: from engineering conversations, existing solutions
   and evidence.

The product is **not yet chosen**. Lupine's architecture alone does not establish a market;
commercial uncertainty stays explicit. Relevant organisations named by the owner: Firmus,
Hydro Tasmania, TasNetworks, UTAS. **Do not steer toward finance, billing, reporting or
general operations roles.**

Owner's background: industrial and production engineering; a beginner in electrical
engineering, computing and software; about 10–12 hours a week. The timeline and the evidence
required at each stage are in `docs/handbook/handbook.md`, Part I.

Lupine began as a payments decision engine (Section 7). That work is **historical context**.

---

## 2. How to teach (every session)

- **One manageable lesson at a time:** explain (concept, units, equations, assumptions) →
  demonstrate (one worked example) → attempt (one exercise; predict first) → check (in the
  owner's own words; investigate mistakes) → record (in the handbook).
- After setting an exercise, **wait for the answer**. Don't reveal it in advance.
- Increase complexity only when the owner can explain the current step.
- Connect fundamentals to energy infrastructure, data centres and Tasmania, and progressively
  to Lupine's code.
- **Don't generate large systems the owner can't understand.** Keep changes small, and explain
  every change made.

---

## 3. Claim labels (use everywhere)

| Label | Meaning |
|---|---|
| **[ASSUMED]** | Taken as true without our own check. Name the source and date. |
| **[SIMULATED]** | Produced by software modelling a system; true only within its assumptions. |
| **[MEASURED]** | Observed with an instrument we used. Record instrument, method, date, uncertainty. |
| **[VERIFIED]** | Checked by an independent method. **Always state the scope.** |

**Software tests are not physical validation.** "Verified by tests" means verified in
simulation only. Payments-era figures and their provenance are in `docs/provenance.md`.

---

## 4. Where things live

| Location | Purpose |
|---|---|
| `README.md` | Introduction, honest status, where to start |
| `CLAUDE.md` | This file: direction, teaching method, coding agreements |
| `docs/handbook/` | Editable learning handbook (`handbook.md`) and preserved PDF editions |
| `docs/architecture.md` | The actual code: what each part does, boundaries, limitations |
| `experiments/` | Reproducible experiment records, setup, raw measurements |
| `research/` | Sourced reading notes, problem observations, conversation summaries (public-safe) |
| `src/`, `tests/` | Working software and its tests |
| `website/` | Public presentation; brand assets in `website/assets/brand/` |

**Raw measurements have one home:** `experiments/<id>/data/`. The handbook and website
reference them and never copy them. Create a folder only when it has real content in it;
don't scaffold empty future modules.

---

## 5. Aiva, Rail and Cloked: concepts kept, implementations may evolve

| Layer | Concept | Implementation today | For energy work |
|---|---|---|---|
| **Aiva** (`src/aiva_lite/`) | Decides what should happen | Weighted sum over payment routes | Pattern only. Engineering limits must be pass/fail feasibility checks **before** any scoring; a weighted sum can trade a safety limit against cost. |
| **Rail** (`src/rail_lite/`) | Executes and reconciles | State machine and evidence rules, domain-neutral | **The active foundation.** |
| **Cloked** (`src/cloked_lite/`) | Preserves decisions and evidence | SHA-256 hash chain, in memory | Partial: proves internal consistency only (see below). |

- No layer leaks logic upward or takes on another layer's job.
- **Don't force an energy problem into payments abstractions** (`MovementRequest`,
  `RouteOption`, urgency weights). Create new models when real engineering requirements
  justify them.
- Preserve the `Cloked` spelling and the `_lite` suffixes.

### Rail-lite: the rules in force (`executor.py`, `outcome.py`)
```
initiated → scored → route_selected → executing → completed | failed | mismatched | uncertain
                                       uncertain → completed | failed | mismatched   (reconcile only)
```
Invalid transitions raise `ValueError`. `assess()` is a pure function of instruction,
observation and `now`.
- **completed** needs both a counterparty `accepted` receipt and a usable reading within tolerance.
- **failed** needs `rejected` or `not_found`, with no usable reading showing the effect
  anyway. Contradictory evidence stays **uncertain**.
- **mismatched**: accepted, but a usable reading is outside tolerance. Not success.
- **uncertain**: everything else. Missing readings are `None`, never zero; stale, pre-settle
  or future-dated readings don't count. No receipt with a matching reading is still uncertain,
  because the effect can't be attributed.
- Only `reconcile()` can leave `uncertain`; `advance_state()` refuses.
- `safe_to_reissue()` is true only when the latest evidence verdict is `failed`: never while
  uncertain, and not for a failure set by hand.
- Known gaps: `Instruction.target` carries **no unit**; there is no real I/O, no timeout, no
  persistence, and the clock is supplied by the caller. The only device is
  `scripts/rail_uncertainty_demo.py`, a **[SIMULATED]** battery controller.

### Cloked-lite
Append-only SHA-256 chain from `genesis`. `verify_chain()` recomputes every hash and checks
the links. **It proves internal consistency only:** a forger who recomputes every later hash
also passes, so tamper-evidence needs the head hash kept elsewhere (not built). It never
proves that a reading was accurate or that an instruction caused an effect.

### Tests and CI
30 deterministic tests in `tests/test_aiva.py`, `test_rail.py` and `test_cloked.py`. CI
(`ci.yml`) **lists test files explicitly**, so a new test file must be added there.
`tests/test_live.py` calls live FX APIs and is advisory, run only by `daily.yml`.

---

## 6. Working agreements

- Work on a branch, in small reviewable commits. Preserve history, observations and corrections.
- New logic ships with tests; keep CI and website deployment green.
- If a change implies a new event, log it to Cloked and cover it in tests.
- **Never mix relocating code with changing behaviour.** Payments-era code stays at its current
  paths until a separate migration (plan in `docs/architecture.md`).
- **Free by default.** Don't add paid services or API dependencies without explaining why.
- **The repository is public.** Keep private personal information out of it: birth data,
  addresses, contact details, private conversation content, confidential partner
  information. Conversation summaries in `research/` need the other person's consent and
  carry no confidential detail.
- **Astrology** is an optional personal planning appendix in the handbook only. Never use it
  as engineering input, and never as a reason to delay work.
- **Safety, until explicitly changed:** 5 V USB power only; no mains work (in Australia that
  requires a licensed electrician); no loose lithium cells; nothing left powered and unattended.
- **Handbook:** edit only the master `docs/handbook/handbook.md`. Build with
  `python scripts/build_handbook.py`; editions are never overwritten. Record a lesson only
  after it is complete. The owner's words go only in `::: yours` boxes.

---

## 7. Earlier payments work (historical: April to October 2026)

Lupine began as "deterministic infrastructure for cross-border value movement", with
Australia → Singapore (AUD→SGD) as its primary corridor. The code still runs at its
original paths:

- `src/aiva_lite/router.py`: 21 modelled payment providers. Their constants are **[ASSUMED]**
  and unverified; reliability values were invented.
- `src/aiva_lite/scorer.py` and `selector.py`: `U = w1·Speed + w2·Cost + w3·Reliability`,
  with urgency weights. Don't expand this to the payments book's 7-term model unless asked.
- `src/data/fx_feed.py`: a 4-source FX feed. `src/api/main.py`: FastAPI with 9 endpoints.
  `/chat` needs a paid API key and is inactive as deployed.
- `scripts/`: `watcher.py`, `backtest.py`, `spread_log.py`, `generate_live_decisions.py`,
  `generate_site_data.py`, `fetch_daily_news.py`. Workflows `watcher.yml` and `daily.yml`
  run them on schedules.

**Don't present their outputs as evidence that an energy product works.** The payments-era
design convention ("premium B2B fintech": slate `#F8FAFC`, navy `#0F172A`, blue `#2563EB`
for the winning route, coral `#EF4444` for rejected ones) applies only to the existing
payments pages. Out of scope unless explicitly named: the payments book's biological/medical
extension.

---

## 8. Conventions

- **Container-style names:** Lupine, Aiva, Rail, Cloked, Keel, Cairn. Names gain meaning
  through the product; don't "clarify" them into functional names.
- **Brand:** the approved mountain, wolf and water logo. Master file:
  `website/assets/brand/lupine-logo-original.webp`; don't recolour or redraw it. Derived
  files sit beside it. Colours sampled from the logo: forest `#1B422E`, teal `#498182`,
  paper `#FEFDF7`. Light themes for new material.
- Determinism, idempotency and verifiable evidence are values, not features.

## 9. Going deeper

`docs/architecture.md` (the code), `docs/handbook/handbook.md` (the learning record),
`docs/provenance.md` (payments-era figures), `experiments/README.md`, `research/README.md`.
`docs/guide.md` and `docs/v0_spec.md` describe the payments-era system.
