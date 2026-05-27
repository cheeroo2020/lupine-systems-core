# Test Results

Daily automated health check records for Lupine Systems V0.
Every entry is written by GitHub Actions — no manual steps needed.

---

## How it works

Every day at **9am UTC** GitHub Actions:
1. Runs 10 deterministic tests against fixed simulation data
2. Fetches the live AUD/SGD rate from [Frankfurter API](https://www.frankfurter.app)
3. Runs 4 live tests against that day's real market rate
4. Writes a dated `.md` file here with full results + raw output
5. Commits and pushes it back to the repo under your account
6. Opens a GitHub Issue automatically if anything fails

---

## Data sources

### Deterministic dataset (fixed, always the same)
Used by `test_aiva.py`, `test_rail.py`, `test_cloked.py`

| Field | Value |
|-------|-------|
| Amount | 500,000 AUD |
| To currency | SGD |
| Urgency levels tested | high, low, normal |

**Routes hardcoded in `src/aiva_lite/router.py`:**

| Route | Time | Cost | Reliability |
|-------|-----:|-----:|------------:|
| Fast Route | 2.5h | 45bps | 0.82 |
| Cheap Route | 18.0h | 12bps | 0.71 |
| Balanced Route | 6.0h | 28bps | 0.93 |

These are fixed so tests are always reproducible — same input, same output, every run.

### Live dataset (changes daily)
Used by `tests/test_live.py`

| Field | Value |
|-------|-------|
| Source | [Frankfurter API](https://www.frankfurter.app) — free, no API key |
| Endpoint | `https://api.frankfurter.app/latest?from=AUD&to=SGD` |
| Updates | Every business day (ECB reference rates) |
| What it tests | That the full V0 pipeline runs correctly against today's real AUD/SGD rate |

The live rate is embedded in the evidence chain and recorded in each daily file — so you can look back and see what the market rate was on any given day.

---

## What each test covers

### `test_aiva.py` — Intelligence layer
| Test | What it checks |
|------|----------------|
| `test_generate_routes_returns_three` | Router always produces exactly 3 candidates |
| `test_high_urgency_favours_fast_route` | Speed weight 50% → Fast Route wins |
| `test_low_urgency_favours_cheap_route` | Cost weight 55% → Cheap Route preferred |
| `test_scores_sum_correctly` | Composite score = exact weighted sum of components |

### `test_rail.py` — Execution layer
| Test | What it checks |
|------|----------------|
| `test_full_execution_completes` | State machine reaches `completed` in 5 steps |
| `test_invalid_transition_raises` | Skipping states raises `ValueError` |
| `test_state_history_tracks_all` | Every state recorded in history in correct order |

### `test_cloked.py` — Evidence layer
| Test | What it checks |
|------|----------------|
| `test_chain_integrity` | 3-entry chain verifies as valid |
| `test_tampered_chain_fails` | Modifying a hash breaks `verify_chain()` |
| `test_genesis_link` | First entry always links to `"genesis"` |

### `test_live.py` — Live FX integration
| Test | What it checks |
|------|----------------|
| `test_frankfurter_api_reachable` | API is online and returning a valid rate |
| `test_live_aud_sgd_high_urgency` | Full pipeline with today's rate, urgency=high |
| `test_live_aud_sgd_low_urgency` | Full pipeline with today's rate, urgency=low |
| `test_live_evidence_chain_with_real_rate` | Evidence chain valid with live rate embedded |

---

## How to find the GitHub Actions run

1. Go to `github.com/cheeroo2020/lupine-systems-core`
2. Click the **Actions** tab
3. Select **Daily Health Check** on the left
4. Click any run to see the full output

---

## Results index

| Date | Result | Tests | AUD/SGD Rate |
|------|--------|-------|--------------|
| [2026-04-21](./2026-04-21.md) | ✅ PASSED | 14/14 | 1 AUD = 0.90993 SGD |
| [2026-04-23](./2026-04-23.md) | ✅ PASSED | 14/14 | 1 AUD = 0.91106 SGD |
| [2026-04-24](./2026-04-24.md) | ✅ PASSED | 10/10 | 1 AUD = 0.91106 SGD |
| [2026-04-25](./2026-04-25.md) | ✅ PASSED | 10/14 | 1 AUD = 0.91191 SGD |
| [2026-04-26](./2026-04-26.md) | ✅ PASSED | 10/14 | 1 AUD = 0.91191 SGD |
| [2026-04-27](./2026-04-27.md) | ✅ PASSED | 10/14 | 1 AUD = 0.91191 SGD |
| [2026-04-28](./2026-04-28.md) | ✅ PASSED | 10/14 | 1 AUD = 0.91535 SGD |
| [2026-04-29](./2026-04-29.md) | ✅ PASSED | 10/14 | 1 AUD = 0.91444 SGD |
| [2026-04-30](./2026-04-30.md) | ✅ PASSED | 10/14 | 1 AUD = 0.91483 SGD |
| [2026-05-01](./2026-05-01.md) | ✅ PASSED | 10/14 | 1 AUD = 0.91222 SGD |
| [2026-05-02](./2026-05-02.md) | ✅ PASSED | 10/14 | 1 AUD = 0.91222 SGD |
| [2026-05-03](./2026-05-03.md) | ✅ PASSED | 10/14 | 1 AUD = 0.914451 SGD |
| [2026-05-04](./2026-05-04.md) | ✅ PASSED | 10/14 | 1 AUD = 0.917364 SGD |
| [2026-05-05](./2026-05-05.md) | ✅ PASSED | 10/14 | 1 AUD = 0.915905 SGD |
| [2026-05-06](./2026-05-06.md) | ✅ PASSED | 10/14 | 1 AUD = 0.916453 SGD |
| [2026-05-07](./2026-05-07.md) | ✅ PASSED | 10/14 | 1 AUD = 0.918239 SGD |
| [2026-05-08](./2026-05-08.md) | ✅ PASSED | 10/14 | 1 AUD = 0.917889 SGD |
| [2026-05-09](./2026-05-09.md) | ✅ PASSED | 10/14 | 1 AUD = 0.917715 SGD |
| [2026-05-10](./2026-05-10.md) | ✅ PASSED | 10/14 | 1 AUD = 0.917663 SGD |
| [2026-05-11](./2026-05-11.md) | ✅ PASSED | 10/14 | 1 AUD = 0.917631 SGD |
| [2026-05-12](./2026-05-12.md) | ✅ PASSED | 10/14 | 1 AUD = 0.919619 SGD |
| [2026-05-13](./2026-05-13.md) | ✅ PASSED | 10/14 | 1 AUD = 0.919394 SGD |
| [2026-05-14](./2026-05-14.md) | ✅ PASSED | 10/14 | 1 AUD = 0.922527 SGD |
| [2026-05-15](./2026-05-15.md) | ✅ PASSED | 10/14 | 1 AUD = 0.921702 SGD |
| [2026-05-16](./2026-05-16.md) | ✅ PASSED | 10/14 | 1 AUD = 0.916282 SGD |
| [2026-05-17](./2026-05-17.md) | ✅ PASSED | 10/14 | 1 AUD = 0.916596 SGD |
| [2026-05-18](./2026-05-18.md) | ✅ PASSED | 10/14 | 1 AUD = 0.914842 SGD |
| [2026-05-19](./2026-05-19.md) | ✅ PASSED | 10/14 | 1 AUD = 0.916134 SGD |
| [2026-05-20](./2026-05-20.md) | ✅ PASSED | 10/14 | 1 AUD = 0.911353 SGD |
| [2026-05-21](./2026-05-21.md) | ✅ PASSED | 10/14 | 1 AUD = 0.912881 SGD |
| [2026-05-22](./2026-05-22.md) | ✅ PASSED | 10/14 | 1 AUD = 0.913097 SGD |
| [2026-05-23](./2026-05-23.md) | ✅ PASSED | 10/14 | 1 AUD = 0.912505 SGD |
| [2026-05-24](./2026-05-24.md) | ✅ PASSED | 10/14 | 1 AUD = 0.912535 SGD |
| [2026-05-25](./2026-05-25.md) | ✅ PASSED | 10/14 | 1 AUD = 0.912844 SGD |
| [2026-05-26](./2026-05-26.md) | ✅ PASSED | 10/14 | 1 AUD = 0.915846 SGD |
| [2026-05-27](./2026-05-27.md) | ✅ PASSED | 10/14 | 1 AUD = 0.915545 SGD |
