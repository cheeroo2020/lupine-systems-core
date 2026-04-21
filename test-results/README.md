# Test Results

This folder contains a daily record of every automated V0 health check run.

---

## How it works

Every day at **9am UTC**, GitHub Actions runs the full V0 test suite automatically.
After the run, the workflow writes a dated `.md` file here, commits it, and pushes it
back to the repo. No manual action needed.

Each file is named `YYYY-MM-DD.md` and contains:
- Overall result (PASSED / FAILED)
- Individual test outcomes
- Run time
- Link to the GitHub Actions run log

---

## Dataset the tests run against

The tests use a fixed in-code simulation dataset — no external database or API.
It represents the V0 demo scenario:

### Movement Request
| Field | Value |
|-------|-------|
| Amount | 500,000 |
| From | AUD |
| To | SGD |
| Urgency | varied per test (high / low / normal) |

### Route Options (hardcoded in `src/aiva_lite/router.py`)
| Route | Time | Cost | Reliability |
|-------|-----:|-----:|------------:|
| Fast Route | 2.5h | 45bps | 0.82 |
| Cheap Route | 18.0h | 12bps | 0.71 |
| Balanced Route | 6.0h | 28bps | 0.93 |

These values are fixed and deterministic — the same inputs always produce the same
scores, which is why they're suitable for a daily regression check.

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

---

## How to find the GitHub Actions run

1. Go to `github.com/cheeroo2020/lupine-systems-core`
2. Click the **Actions** tab
3. Select **Daily Health Check** on the left
4. Click any run to see the full pytest output

---

## File index

| Date | Result | Tests |
|------|--------|-------|
| [2026-04-21](./2026-04-21.md) | ✅ PASSED | 10/10 |
