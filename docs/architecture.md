# Lupine — architecture of the actual code

What the code in this repository really does, how the parts depend on each other, and
where each one falls short. Written 16 October 2026 at commit `eff229b` and checked against
the code, not the plans. When the code and this file disagree, the code is right and this
file needs a correction.

Labels used: **[SIMULATED]** software only · **[MEASURED]** our own instrument ·
**[ASSUMED]** taken from a source or chosen without checking · **[VERIFIED]** checked
independently, with the scope stated.

---

## 1. The picture

```
                      ┌──────────────────────── Lupine concepts ───────────────────────┐
                      │   Aiva (decides)   →   Rail (executes, reconciles)   →  Cloked │
                      │                                                     (evidence) │
                      └────────────────────────────────────────────────────────────────┘
 Active foundation    src/rail_lite/outcome.py, executor.py      src/cloked_lite/logger.py
 (domain-neutral)     src/models/schemas.py: Instruction, Observation, Receipt, Assessment
                      scripts/rail_uncertainty_demo.py  [SIMULATED battery controller]

 Earlier payments     src/aiva_lite/{router,scorer,selector}.py    src/data/fx_feed.py
 work (historical)    src/api/main.py    scripts/{watcher,backtest,spread_log,
                      generate_live_decisions,generate_site_data,fetch_daily_news}.py
                      .github/workflows/{watcher,daily}.yml     website/payments/ dashboard
```

Nothing in the repository connects to real equipment. **Nothing has been physically tested.**

---

## 2. Rail: the active foundation (`src/rail_lite/`)

**What it does.** After an instruction is sent, Rail decides what the evidence supports, and
nothing more.

- `outcome.py` holds `assess(instruction, observation, now)`. It is a pure function: the same
  evidence always gives the same verdict, and the verdict records its reason.
- The evidence is a **receipt** (what the other side says: `accepted`, `rejected`,
  `not_found`, `fenced_no_execution`, or `None` when nothing came back) plus a **reading** (a
  value and the time it was taken, or `None`).
- **Identity comes first.** The receipt must name the instruction, the reading must measure
  the instruction's `resource`, and both must come from the device `session` the instruction
  was sent to. If not, the verdict is uncertain.
- `not_found` is weak: it stays uncertain, because the instruction may be delayed, queued
  elsewhere or forgotten after a restart. Only `rejected` or `fenced_no_execution` (the device
  guarantees it did not and can never run) can support `failed`.
- A reading only counts if it is present, a number, not from the future, taken after the
  instruction's settle time, and no older than its maximum age.
- `executor.py` holds the state machine:
  ```
  initiated → scored → route_selected → executing → completed | failed | mismatched | uncertain
                                         uncertain → completed | failed | mismatched   (reconcile only)
  ```
  `record_outcome()` makes the first verdict. `reconcile()` is the only way out of
  `uncertain`; `advance_state()` refuses to move an uncertain execution.
  `safe_to_reissue()` is true only when the latest evidence verdict is `failed`.
- Every verdict is kept in `ExecutionState.assessments`.

**Status.** **[VERIFIED] by 27 tests in `tests/test_rail.py`, in simulation only.** The tests
include regressions for paths that once allowed a retry without evidence: three found in
review on 16 Oct 2026, and five found against the textbook on 17 Oct 2026 ("not found" treated
as proof; evidence identity not checked). `scripts/rail_uncertainty_demo.py` runs nine cases
against a pretend battery controller
**[SIMULATED]**; it models no real device or protocol.

**Limitations.**

- `Instruction.target` and `tolerance` are bare numbers with **no unit**. "50" could be W or kW.
- There is no real communication, no timeout handling and no persistence: state lives in memory
  and is lost when the process ends. The clock is supplied by the caller.
- The first three states (`scored`, `route_selected`) are payments vocabulary. An energy
  instruction doesn't pass through route scoring.
- Restart behaviour (what Rail knows after a crash) is not designed yet. It is scheduled for
  Apr–Jun 2027.

## 3. Cloked: evidence (`src/cloked_lite/logger.py`)

**What it does.** An append-only list of entries. Each entry stores the SHA-256 hash of its
contents and the previous entry's hash, starting from `"genesis"`. `verify_chain()` recomputes
every hash and checks every link.

**Status.** **[VERIFIED] by 5 tests in `tests/test_cloked.py`.** On 16 Oct 2026 a further check
showed that **a forger who rebuilds the chain, recomputing every later hash, also passes
`verify_chain()`**. The chain only exposes tampering when compared with a copy of the final
hash kept somewhere the forger can't reach.

**Limitations.** In memory only; no stored or published head hash; no signatures. A valid
chain shows records are consistent with each other. It never shows that a reading was
accurate or that an instruction caused an effect.

Events used: `request_created`, `routes_generated`, `routes_scored`, `execution_completed`
(payments API), and `instruction_issued`, `outcome_assessed`, `reconciliation_attempted`
(Rail demo and tests).

## 4. Aiva: decisions (`src/aiva_lite/`), payments-era

**What it does.**

- `router.py` builds candidate payment routes. With a live FX rate it returns 21 modelled
  providers; without one it returns 3 simulated routes.
- `scorer.py` computes `U = w1·Speed + w2·Cost + w3·Reliability`, min-max normalised, with
  weights set by urgency (low, normal, high, critical).
- `selector.py` picks the highest U and writes a plain-English rationale.

**Status.** The code runs, and 4 tests in `tests/test_aiva.py` cover it. **Its inputs are
[ASSUMED]:** all 21 provider costs and times are hardcoded constants with no checkable source,
and the reliability values were invented (see `docs/provenance.md`).

**What energy work needs instead.** Engineering limits (current, temperature, state of charge,
ramp rate) are pass/fail constraints. They must be checked **before** any scoring, because a
weighted sum can trade a safety limit against cost. None of this exists yet.

## 5. Data models (`src/models/schemas.py`)

| Domain-neutral (reusable) | Payments-specific |
|---|---|
| `ExecutionStatus`, `ExecutionState`, `Receipt`, `Instruction`, `Observation`, `Assessment`, `EvidenceEntry`, `EvidenceLog` | `Urgency`, `MovementRequest`, `RouteOption`, `DecisionScore` |

Both kinds live in one file today. Splitting them is migration step M4 (section 9).

## 6. Tools

| File | Purpose | Notes |
|---|---|---|
| `scripts/rail_uncertainty_demo.py` | Nine Rail cases against a pretend battery | **[SIMULATED]**. Run: `PYTHONPATH=. python scripts/rail_uncertainty_demo.py` |
| `scripts/build_rail_rules.py` | Runs Rail's real code over the 60 situations in the website's "Try the rules" panel and writes `website/assets/rail-rules.json` | A test fails if the file and the code disagree |
| `scripts/build_handbook.py` | Handbook master → paginated PDF edition | Free (`reportlab`). Never overwrites an edition |

---

## 7. Earlier payments work: inventory and dependencies

All of this still runs. **None of its output is evidence that an energy product works.**

| Part | What it does | Status and limitations |
|---|---|---|
| `src/data/fx_feed.py` | AUD/SGD rate from 4 free public sources, with fallback | Values **[MEASURED]** as published. Sources give a *date*, not a fixing time |
| `src/api/main.py` | FastAPI, **9 endpoints**: create-movement, get-routes, score-routes, execute, log, recommend, healthz, chat, `/` | Stores everything in a dict in memory, so all of it is lost on restart. `/execute` uses `simulate_full_execution()`, which always succeeds. `/recommend` calls Frankfurter directly, not `fx_feed`. **`/chat` needs a paid Anthropic API key and the `anthropic` package**, neither of which is configured, so it is inactive. Deploy config: `render.yaml` |
| `scripts/watcher.py` | Hourly STRIKE/WATCH/HOLD/NEUTRAL signal from rate history and news | **The STRIKE GitHub-issue step has never worked.** It requests the labels `watcher` and `strike`, which don't exist in the repository. There have been 434 STRIKE signals since 2 May 2026 and **0 issues**, and the failure was hidden by `continue-on-error` |
| `scripts/spread_log.py` | Disagreement between published FX values, collected in one run | The only measured dataset: 695+ observations since 3 Aug 2026. **Not** aligned to one instant (corrected 16 Oct 2026). Each row also stores 21 modelled provider costs, so the log is about 1.3 MB |
| `scripts/backtest.py` | 90-day replay of the router over ECB rates | Rates are **[MEASURED]**; the routing applied to them uses **[ASSUMED]** constants |
| `scripts/generate_live_decisions.py` | Daily decisions JSON for the dashboard | Uses the **[ASSUMED]** constants |
| `scripts/generate_site_data.py` | `news.json` and `health.json`; reruns the backtest if stale | — |
| `scripts/fetch_daily_news.py` | Daily payments/FX news digest from RSS feeds | Free; no key needed |

### Dependency map

```
src/models/schemas.py ◄── every module below
src/aiva_lite/router.py   ◄── api/main.py, scripts/backtest.py, generate_live_decisions.py,
                              spread_log.py, tests/test_aiva.py, tests/test_live.py
src/aiva_lite/scorer.py   ◄── api/main.py, backtest.py, generate_live_decisions.py, tests (aiva, live)
src/aiva_lite/selector.py ◄── same as scorer.py
src/data/fx_feed.py       ◄── generate_live_decisions.py, spread_log.py, watcher.py, tests/test_live.py
src/rail_lite/executor.py ◄── api/main.py (simulate_full_execution), rail_uncertainty_demo.py, tests/test_rail.py
src/cloked_lite/logger.py ◄── api/main.py, generate_live_decisions.py, watcher.py,
                              rail_uncertainty_demo.py, tests (cloked, live)

Workflows → scripts:  daily.yml   → tests/*, fetch_daily_news.py, generate_live_decisions.py,
                                    generate_site_data.py (→ backtest.py)
                      watcher.yml → watcher.py, spread_log.py
                      render.yaml → src.api.main:app
Website → data:       only website/payments/index.html reads website/data/ (agent_signal, backtest,
                      health, live_decisions, news). No page links into source files.
```

---

## 8. Automation inventory and recommendation

| Workflow | Trigger | What it does | Writes | Recommendation |
|---|---|---|---|---|
| `ci.yml` | Every push; PRs to `main` | Deterministic tests (files listed explicitly) | Nothing | **Keep.** Add new test files to its list |
| `pages.yml` | Push to `main`; manual; dispatched by the other two | Deploys `website/` to GitHub Pages | The site | **Keep** |
| `watcher.yml` | Hourly cron at :30 (about 5 runs a day in practice) | Payments signal; FX spread log; commits; dispatches Pages | `agent_signal.json`, `spread_log.jsonl`, `spread_summary.json` | **Manual-only for the signal.** Decide separately about the spread log (below) |
| `daily.yml` | Hourly cron plus 08:00 UTC; skips once the day is done | Tests (duplicating CI), live FX tests, news, live decisions, site data, backtest; commits; dispatches Pages | `test-results/`, `daily-news/`, `website/data/` | **Manual-only**, but only after the website labels the payments dashboard as historical |

**Why change them.** Of 1,924 commits on `main`, **1,746 (91%) are automated** `watcher:` or
`daily:` commits. In the last 30 days there were 176 of them. They bury real work in the
history, and they keep the payments dashboard looking current when it is not the active
direction.

**What stopping them would do to data collection.**

- **Spread log:** the series stops growing. All existing observations are kept unchanged and
  the summary freezes at its last values. It is the only measured dataset in the repository,
  so there are three options: (a) keep it on a reduced schedule, such as every 6 hours, for
  continuity; (b) freeze it, as a finished payments-era record; (c) run it manually when
  needed. **This decision is yours; nothing has been changed.**
- **Watcher signal:** the dashboard's watcher panel keeps showing its last signal, so it goes
  stale unless the page is labelled historical. No issues are lost, because none were ever
  created.
- **Daily pipeline:** `test-results/` daily files and `daily-news/` stop. The dashboard's
  health, live decisions, news and backtest freeze at their last run. CI still tests every
  push.

**Found while inventorying:**

1. The watcher's issue step fails silently (missing labels).
2. `daily.yml` writes a hardcoded `/14` test total into `test-results/README.md`; the suite
   now has 36 deterministic tests.
3. A comment in `watcher.yml` repeated the corrected "same instant" claim. It was fixed on
   16 Oct 2026; comment only, no change to behaviour.

**Recommended order:** (1) a website change labelling the payments material historical and
presenting the energy direction; (2) switch `watcher.yml` and `daily.yml` to manual-only, with
your decision on the spread log; (3) the code migration below.

---

## 9. Migration plan (prepared, not executed)

The goal is to move payments-era code into a clearly named place without changing what any
of it does. Each step is its own commit, with tests and CI green before the next.
**Relocating code is never mixed with changing behaviour.**

| Step | Change | Must update at the same time |
|---|---|---|
| M1 | Website labels payments material historical (see section 8). **Done 16 Oct 2026:** energy front page; dashboard moved to `website/payments/` with a historical banner. Per-page banners on the essays, lessons, Cairn and slide remain | Website pages; README and `watcher.yml` dashboard links |
| M2 | `watcher.yml` and `daily.yml` → `workflow_dispatch` only | The automation map in the README |
| M3 | Move `src/data/fx_feed.py`, `src/aiva_lite/router.py`, `scorer.py`, `selector.py` and `src/api/main.py` under `src/payments/` | All imports in section 7's map; `tests/test_aiva.py`, `test_live.py`; `render.yaml` start command; README and CLAUDE.md paths |
| M4 | Split `schemas.py` into domain-neutral execution/evidence models and `src/payments/models.py` | Every `from src.models.schemas import`; tests |
| M5 | Move the payments scripts to `scripts/payments/` | `daily.yml`, `watcher.yml` and `generate_site_data.py` (it calls `backtest.py` by path); README quick start |
| — | **Do not move** `website/data/` | `website/payments/index.html` reads it by relative path (`../data/`) |

What becomes of `src/aiva_lite/` after M3 is an open design question. It should be decided
when an energy requirement shows what Aiva must actually decide.

---

## 10. Corrections to this file

| Date | Was | Now |
|---|---|---|
| — | No corrections yet | — |
