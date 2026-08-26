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
| [2026-05-28](./2026-05-28.md) | ✅ PASSED | 10/14 | 1 AUD = 0.911886 SGD |
| [2026-05-29](./2026-05-29.md) | ✅ PASSED | 10/14 | 1 AUD = 0.911886 SGD |
| [2026-05-30](./2026-05-30.md) | ✅ PASSED | 10/14 | 1 AUD = 0.915993 SGD |
| [2026-05-31](./2026-05-31.md) | ✅ PASSED | 10/14 | 1 AUD = 0.915519 SGD |
| [2026-06-01](./2026-06-01.md) | ✅ PASSED | 10/14 | 1 AUD = 0.916406 SGD |
| [2026-06-02](./2026-06-02.md) | ✅ PASSED | 10/14 | 1 AUD = 0.916406 SGD |
| [2026-06-03](./2026-06-03.md) | ✅ PASSED | 10/14 | 1 AUD = 0.918114 SGD |
| [2026-06-04](./2026-06-04.md) | ✅ PASSED | 10/14 | 1 AUD = 0.917019 SGD |
| [2026-06-05](./2026-06-05.md) | ✅ PASSED | 10/14 | 1 AUD = 0.916274 SGD |
| [2026-06-06](./2026-06-06.md) | ✅ PASSED | 10/14 | 1 AUD = 0.913805 SGD |
| [2026-06-07](./2026-06-07.md) | ✅ PASSED | 10/14 | 1 AUD = 0.914333 SGD |
| [2026-06-08](./2026-06-08.md) | ✅ PASSED | 10/14 | 1 AUD = 0.911116 SGD |
| [2026-06-09](./2026-06-09.md) | ✅ PASSED | 10/14 | 1 AUD = 0.908861 SGD |
| [2026-06-10](./2026-06-10.md) | ✅ PASSED | 10/14 | 1 AUD = 0.905997 SGD |
| [2026-06-11](./2026-06-11.md) | ✅ PASSED | 10/14 | 1 AUD = 0.905997 SGD |
| [2026-06-12](./2026-06-12.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901952 SGD |
| [2026-06-13](./2026-06-13.md) | ✅ PASSED | 10/14 | 1 AUD = 0.904275 SGD |
| [2026-06-14](./2026-06-14.md) | ✅ PASSED | 10/14 | 1 AUD = 0.904187 SGD |
| [2026-06-15](./2026-06-15.md) | ✅ PASSED | 10/14 | 1 AUD = 0.904187 SGD |
| [2026-06-16](./2026-06-16.md) | ✅ PASSED | 10/14 | 1 AUD = 0.906928 SGD |
| [2026-06-17](./2026-06-17.md) | ✅ PASSED | 10/14 | 1 AUD = 0.906928 SGD |
| [2026-06-18](./2026-06-18.md) | ✅ PASSED | 10/14 | 1 AUD = 0.906366 SGD |
| [2026-06-19](./2026-06-19.md) | ✅ PASSED | 10/14 | 1 AUD = 0.905195 SGD |
| [2026-06-20](./2026-06-20.md) | ✅ PASSED | 10/14 | 1 AUD = 0.905775 SGD |
| [2026-06-21](./2026-06-21.md) | ✅ PASSED | 10/14 | 1 AUD = 0.905746 SGD |
| [2026-06-22](./2026-06-22.md) | ✅ PASSED | 10/14 | 1 AUD = 0.905746 SGD |
| [2026-06-23](./2026-06-23.md) | ✅ PASSED | 10/14 | 1 AUD = 0.9056 SGD |
| [2026-06-24](./2026-06-24.md) | ✅ PASSED | 10/14 | 1 AUD = 0.898193 SGD |
| [2026-06-25](./2026-06-25.md) | ✅ PASSED | 10/14 | 1 AUD = 0.895014 SGD |
| [2026-06-26](./2026-06-26.md) | ✅ PASSED | 10/14 | 1 AUD = 0.894919 SGD |
| [2026-06-27](./2026-06-27.md) | ✅ PASSED | 10/14 | 1 AUD = 0.893056 SGD |
| [2026-06-28](./2026-06-28.md) | ✅ PASSED | 10/14 | 1 AUD = 0.893056 SGD |
| [2026-06-29](./2026-06-29.md) | ✅ PASSED | 10/14 | 1 AUD = 0.893148 SGD |
| [2026-06-30](./2026-06-30.md) | ✅ PASSED | 10/14 | 1 AUD = 0.890851 SGD |
| [2026-07-01](./2026-07-01.md) | ✅ PASSED | 10/14 | 1 AUD = 0.892624 SGD |
| [2026-07-02](./2026-07-02.md) | ✅ PASSED | 10/14 | 1 AUD = 0.893614 SGD |
| [2026-07-03](./2026-07-03.md) | ✅ PASSED | 10/14 | 1 AUD = 0.893393 SGD |
| [2026-07-04](./2026-07-04.md) | ✅ PASSED | 10/14 | 1 AUD = 0.895606 SGD |
| [2026-07-05](./2026-07-05.md) | ✅ PASSED | 10/14 | 1 AUD = 0.89538 SGD |
| [2026-07-06](./2026-07-06.md) | ✅ PASSED | 10/14 | 1 AUD = 0.895944 SGD |
| [2026-07-07](./2026-07-07.md) | ✅ PASSED | 10/14 | 1 AUD = 0.895944 SGD |
| [2026-07-08](./2026-07-08.md) | ✅ PASSED | 10/14 | 1 AUD = 0.896994 SGD |
| [2026-07-09](./2026-07-09.md) | ✅ PASSED | 10/14 | 1 AUD = 0.896195 SGD |
| [2026-07-10](./2026-07-10.md) | ✅ PASSED | 10/14 | 1 AUD = 0.897009 SGD |
| [2026-07-11](./2026-07-11.md) | ✅ PASSED | 10/14 | 1 AUD = 0.897215 SGD |
| [2026-07-12](./2026-07-12.md) | ✅ PASSED | 10/14 | 1 AUD = 0.897063 SGD |
| [2026-07-13](./2026-07-13.md) | ✅ PASSED | 10/14 | 1 AUD = 0.897189 SGD |
| [2026-07-14](./2026-07-14.md) | ✅ PASSED | 10/14 | 1 AUD = 0.896647 SGD |
| [2026-07-15](./2026-07-15.md) | ✅ PASSED | 10/14 | 1 AUD = 0.898787 SGD |
| [2026-07-16](./2026-07-16.md) | ✅ PASSED | 10/14 | 1 AUD = 0.902558 SGD |
| [2026-07-17](./2026-07-17.md) | ✅ PASSED | 10/14 | 1 AUD = 0.903071 SGD |
| [2026-07-18](./2026-07-18.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901503 SGD |
| [2026-07-19](./2026-07-19.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901456 SGD |
| [2026-07-20](./2026-07-20.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901342 SGD |
| [2026-07-21](./2026-07-21.md) | ✅ PASSED | 10/14 | 1 AUD = 0.90406 SGD |
| [2026-07-22](./2026-07-22.md) | ✅ PASSED | 10/14 | 1 AUD = 0.904706 SGD |
| [2026-07-23](./2026-07-23.md) | ✅ PASSED | 10/14 | 1 AUD = 0.902999 SGD |
| [2026-07-24](./2026-07-24.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901666 SGD |
| [2026-07-25](./2026-07-25.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901637 SGD |
| [2026-07-26](./2026-07-26.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901655 SGD |
| [2026-07-27](./2026-07-27.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901832 SGD |
| [2026-07-28](./2026-07-28.md) | ✅ PASSED | 10/14 | 1 AUD = 0.902787 SGD |
| [2026-07-29](./2026-07-29.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901462 SGD |
| [2026-07-30](./2026-07-30.md) | ✅ PASSED | 10/14 | 1 AUD = 0.896985 SGD |
| [2026-07-31](./2026-07-31.md) | ✅ PASSED | 10/14 | 1 AUD = 0.899572 SGD |
| [2026-08-01](./2026-08-01.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901053 SGD |
| [2026-08-02](./2026-08-02.md) | ✅ PASSED | 10/14 | 1 AUD = 0.901023 SGD |
| [2026-08-03](./2026-08-03.md) | ✅ PASSED | 10/14 | 1 AUD = 0.902119 SGD |
| [2026-08-04](./2026-08-04.md) | ✅ PASSED | 10/14 | 1 AUD = 0.902119 SGD |
| [2026-08-05](./2026-08-05.md) | ✅ PASSED | 10/14 | 1 AUD = 0.902158 SGD |
| [2026-08-06](./2026-08-06.md) | ✅ PASSED | 10/14 | 1 AUD = 0.903705 SGD |
| [2026-08-07](./2026-08-07.md) | ✅ PASSED | 10/14 | 1 AUD = 0.902728 SGD |
| [2026-08-08](./2026-08-08.md) | ✅ PASSED | 10/14 | 1 AUD = 0.902856 SGD |
| [2026-08-09](./2026-08-09.md) | ✅ PASSED | 10/14 | 1 AUD = 0.902685 SGD |
| [2026-08-10](./2026-08-10.md) | ✅ PASSED | 10/14 | 1 AUD = 0.90268 SGD |
| [2026-08-11](./2026-08-11.md) | ✅ PASSED | 10/14 | 1 AUD = 0.903667 SGD |
| [2026-08-12](./2026-08-12.md) | ✅ PASSED | 10/14 | 1 AUD = 0.903952 SGD |
| [2026-08-13](./2026-08-13.md) | ✅ PASSED | 10/14 | 1 AUD = 0.904248 SGD |
| [2026-08-14](./2026-08-14.md) | ✅ PASSED | 10/14 | 1 AUD = 0.903563 SGD |
| [2026-08-15](./2026-08-15.md) | ✅ PASSED | 10/14 | 1 AUD = 0.905395 SGD |
| [2026-08-16](./2026-08-16.md) | ✅ PASSED | 10/14 | 1 AUD = 0.905072 SGD |
| [2026-08-17](./2026-08-17.md) | ✅ PASSED | 10/14 | 1 AUD = 0.905891 SGD |
| [2026-08-18](./2026-08-18.md) | ✅ PASSED | 10/14 | 1 AUD = 0.908312 SGD |
| [2026-08-19](./2026-08-19.md) | ✅ PASSED | 10/14 | 1 AUD = 0.907753 SGD |
| [2026-08-20](./2026-08-20.md) | ✅ PASSED | 10/14 | 1 AUD = 0.904986 SGD |
| [2026-08-21](./2026-08-21.md) | ✅ PASSED | 10/14 | 1 AUD = 0.905313 SGD |
| [2026-08-22](./2026-08-22.md) | ✅ PASSED | 10/14 | 1 AUD = 0.90803 SGD |
| [2026-08-23](./2026-08-23.md) | ✅ PASSED | 10/14 | 1 AUD = 0.908914 SGD |
| [2026-08-24](./2026-08-24.md) | ✅ PASSED | 10/14 | 1 AUD = 0.909734 SGD |
| [2026-08-25](./2026-08-25.md) | ✅ PASSED | 10/14 | 1 AUD = 0.90933 SGD |
| [2026-08-26](./2026-08-26.md) | ✅ PASSED | 10/14 | 1 AUD = 0.90867 SGD |
