# Provenance manifest

Every number Lupine publishes, and where it actually came from.

**Rule:** a figure may only be described as *measured* if this file names the
source, the retrieval method, and a date. Everything else is *modelled*,
*cited*, or *unverified*, and must be labelled as such wherever it appears.

This file exists because in July 2026 the essay published a set of basis-point
figures that had been invented to make a chart look convincing, and presented
them as observed. The manifest is the control that stops that recurring.

Last audited: **2026-08-03**

---

## Status vocabulary

| Status | Meaning |
|---|---|
| **measured** | Observed by our own instrumentation. Source, method and timestamp recorded. |
| **cited** | Taken from a named external document we have read. |
| **modelled** | A constant we chose. Plausible, possibly right, not observed. |
| **unverified** | Claimed source exists but has not been checked against. |
| **fabricated** | Invented. Must be removed or relabelled on sight. |

---

## 1. Measured — our own instrumentation

| Figure | Status | Source | Notes |
|---|---|---|---|
| AUD/SGD mid-market rate | **measured** | `src/data/fx_feed.py`, 4 public sources | Timestamped per fetch |
| Cross-source dispersion (bps) | **measured** | `scripts/spread_log.py`, hourly | First obs 2026-08-03: **4.32 bps** across 3 reachable sources |
| Source staleness spread | **measured** | `spread_log.jsonl` | First obs: source dates spanned 2026-07-31 → 08-03 |
| Backtest FX series | **measured** | Frankfurter/ECB historical, 83 trading days | Rates are real; the routing applied to them is modelled |
| Watcher z-score / percentile | **measured** | `scripts/watcher.py`, 60-day window | Derived from measured rates |
| Test pass rate | **measured** | CI, `test-results/` | 10/10 deterministic |

**Not yet citable.** `spread_summary.json` refuses to mark the dataset citable
below 30 observations. At hourly cadence that is roughly two days.

---

## 2. Modelled — constants in `src/aiva_lite/router.py`

All 21 provider entries are **hardcoded constants**, not live quotes. We hold no
quote API for any provider. The file's source comment reads:

> `Sources: Wise public fee calculator, Airwallex/Nium business pricing,`
> `OFX/WorldFirst published rates, ANZ/CBA SWIFT fee schedules (2025).`

That comment names no URL, no retrieval date, and no figure that can be checked
against. **It was written inside this project**, so citing it back as evidence is
circular. Every row below is therefore `unverified` until someone checks it.

| Provider | bps | hours | reliability | Status |
|---|--:|--:|--:|---|
| Nium | 25 | 2 | 0.87 | unverified |
| Airwallex | 30 | 3 | 0.92 | unverified |
| WorldFirst | 35 | 24 | 0.90 | unverified |
| Revolut Business | 40 | 2 | 0.86 | unverified |
| Wise | 45 | 1 | 0.95 | unverified |
| TorFX | 45 | 24 | 0.88 | unverified |
| OFX | 50 | 24 | 0.91 | unverified |
| CurrencyFair | 55 | 48 | 0.84 | unverified |
| DBS Remit | 80 | 18 | 0.90 | unverified |
| XE Money Transfer | 90 | 48 | 0.86 | unverified |
| Western Union | 120 | 24 | 0.83 | unverified |
| MoneyGram | 160 | 48 | 0.79 | unverified |
| HSBC Premier | 150 | 24 | 0.93 | unverified |
| Citibank | 180 | 24 | 0.91 | unverified |
| ANZ International | 200 | 36 | 0.92 | unverified |
| NAB International | 210 | 36 | 0.92 | unverified |
| Westpac International | 215 | 36 | 0.91 | unverified |
| CBA International | 225 | 36 | 0.91 | unverified |
| OCBC Wire | 200 | 24 | 0.92 | unverified |
| UOB Wire | 205 | 24 | 0.92 | unverified |
| Bank SWIFT | 250.4 | 36 | 0.88 | modelled (250 spread + A$22 wire / A$500K) |

**Reliability scores are the weakest column in the system.** No provider
publishes a failure rate. These are invented and drive 30–40% of every routing
decision. They should be labelled `modelled` in any external material.

**Consequence:** the "saves ~A$10,270 per transfer" figure on the public site is
`45 bps vs 250.4 bps` — a difference between two unverified constants. It is not
a measured saving.

---

## 3. Cited — external documents

Genuinely sourced. These are reproduced as primary text in
`docs/lupine_master_study_pack (1).html`.

| Figure | Status | Source |
|---|---|---|
| Wise take rate 0.77 / 0.73 / 0.66 % | **cited** | Wise IPO prospectus 2021, pp. 77–78 |
| Wise cross-currency take rate 0.70 % | **cited** | Wise IPO prospectus 2021 |
| Wise: 63 licences, 12 countries, 2,500+ routes | **cited** | Wise IPO prospectus 2021, pp. 49–51 |
| Wise: UK FPS fees cut nine-fold, <20s transfers | **cited** | Wise IPO prospectus 2021 |
| Wise: Hungary prices −14 %, instant 17 % → 82 % | **cited** | Wise IPO prospectus 2021 |
| Wise: ~50 % of traded volume ML-predicted | **cited** | Wise IPO prospectus 2021 |
| Remitly: 1,700+ corridors, 115+ receive countries | **cited** | Remitly Form S-1 2021, pp. 16–19 |
| Remitly: >75 % of 2020 transactions under 1 hour | **cited** | Remitly Form S-1 2021 |
| Adyen: six live data centres, real-time rerouting | **cited** | Adyen IPO prospectus 2018, p. 96 |
| Adyen: card networks $23.0tn purchase volume 2017 | **cited** | Adyen IPO prospectus 2018 (via Nilson) |
| 8-component FX formula `S0+dS+F+V+L+C+D+R` | **cited** | Study pack, P1-Ch4 — **formula only, no values** |
| Exposure `σ√t` | **cited** | Study pack, P1-Ch4 |
| RTGS window hours (RITS / TARGET2 / Fedwire) | **cited** | Study pack, P1-Ch1–2 |

---

## 4. Corrected — errors found and fixed

| Claim | Was published as | Actually | Fixed |
|---|---|---|---|
| Corridor latency 2.5 h → 11 d | "Australia → Singapore" | Study pack states **AU → SG → DE**, a three-leg corridor | 2026-08-03 |
| Ratio best:worst **106×** | AU→SG | Holds only for AU→SG→DE | 2026-08-03 |
| FX split 12 / 4 / 9 / 6 / 7 / 11 / 5 bps | "degradation from interbank spot" | **fabricated** — study pack contains zero bps figures | 2026-08-03 |
| "42 bps hidden · A$2,100" | measured | **fabricated** — derived from the above | 2026-08-03 |
| EC2 | "general availability, 2006" | Public **beta** 2006; GA 2008 | 2026-08-03 |
| Containerisation $5.86 → $0.16/ton | cited | Quoted from recall; widely attributed to Levinson, *The Box* — **not checked against a copy** | flagged 2026-08-03 |

---

## 5. Open — what would close the gaps

| Gap | How to close it |
|---|---|
| Corridor cost, AU→SG | World Bank *Remittance Prices Worldwide* — quarterly, measured, published methodology. Covers retail rather than A$500K business, so it supports a narrower claim than we were making. |
| Corridor latency | SWIFT gpi publishes aggregate credited-within-window statistics. |
| Provider spreads | **Best option.** Log mid-market against each provider's published rate daily. After ~30 days this becomes our own measured dataset — the one number nobody else publishes. `scripts/spread_log.py` is the start; it needs provider rate ingestion to complete. |
| Provider reliability | No public source exists. Either drop the dimension from external claims or label it modelled everywhere. |
| Containerisation figures | Check against Levinson, *The Box*, or Bernhofen et al. (2016). |

---

## 6. Rule for anything published from here

1. If it is not in section 1, it is not **measured** and may not be described as such.
2. Section 2 constants must carry the word **modelled** wherever they appear externally.
3. Section 3 figures must name the document.
4. Any new figure gets a row here **before** it goes on a page.
