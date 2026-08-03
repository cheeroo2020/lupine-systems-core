# II. What Non-Determinism Costs

*Deterministic Value — Chapter II of VII*
*Draft · Chirantan Gogoi · Lupine Systems*

---

Chapter I argued that value movement is the last major flow still managed reactively. This
chapter is about what that costs, however it has to begin with an admission, because the
honest answer to "what does it cost" is that **almost nobody knows, including the people
charging it.**

That is not a rhetorical opening. It is the finding.

---

## 2.1 · The rate is not a number

The number you are quoted is a single figure. The rate you actually pay is the sum of eight
components:

> **Effective rate = S₀ + ΔS + F + V + L + C + D + R**

| | Component | What it is |
|---|---|---|
| S₀ | Interbank spot | What banks trade at, at scale |
| ΔS | Spread | The liquidity provider's margin |
| F | Forward points | The interest rate differential between the two currencies |
| V | Volatility premium | Price risk while the money is in flight |
| L | Liquidity premium | A wider spread when the pool is thin |
| C | Corridor cost | Costs specific to this path |
| D | Delay premium | The price impact of latency |
| R | Compliance buffer | Added on corridors judged higher risk |

Two of these are normally visible to the payer, whereas six are not. That is the structural
point, and it does not depend on knowing their sizes.

**What we cannot tell you is the split.** As per the source material, the formula is given and
the values are not. No basis-point decomposition for the Australia to Singapore corridor has
been published by anyone, as far as we can find, and any figure quoted for one here would be
invented. An earlier draft of this essay did exactly that, which is the reason this project now
maintains a provenance manifest.

---

## 2.2 · What can be established

Three things about the cost side can be stated with a source behind them.

**The market's own all-in price is roughly 70 basis points.** Wise's 2021 prospectus discloses
a cross-currency take rate of 0.70%, 0.68% and 0.64% for FY2021, FY2020 and FY2019, with a
total take rate of 0.77% in FY2021. This is audited, published, and covers a business moving
£5bn a month across 2,500 currency routes. It is the closest thing the industry has to an
honest benchmark, and it is worth holding against any provider's quoted headline.

**Integration collapses cost, and by a lot.** The same prospectus states that connecting
directly to the UK Faster Payments Service reduced Wise's partner bank fees **nine-fold** and
brought transfer times under twenty seconds. Integrating with the Hungarian central bank cut
customer prices 14% on average and took instant transfers from 17% to 82% of volume. These are
not projections, they are reported outcomes, and they establish that the cost is structural
rather than natural.

**Nobody publishes the decomposition.** Wise reports a take rate. Remitly reports corridor
counts and speed. Adyen reports platform metrics. None of them break the effective rate into
its components for a given corridor on a given day, because there is no commercial reason to.

---

## 2.3 · Delay is one of the components

The most under-recognised term in the stack is **D**, the delay premium, and the reason it
matters is that it does not stand alone.

Exposure to price movement while the money is in flight is:

> **Exposure = σ × √t**

Volatility multiplied by the square root of settlement time. The square root is the whole
insight. Exposure grows **non-linearly**, so quadrupling the settlement time only doubles the
damage, which means the first hours of delay are disproportionately expensive compared with the
last ones.

| Settlement time | Exposure multiple |
|---|---|
| 1 hour | 1.00 × σ |
| 4 hours | 2.00 × σ |
| 16 hours | 4.00 × σ |
| 36 hours | 6.00 × σ |

There is a chain reaction here that is easy to miss. Delay (D) increases the time in flight,
which increases volatility exposure (V), which liquidity providers price into a wider spread
(ΔS). The three terms are not independent, and a model that scores latency and cost as separate
dimensions will systematically misprice slow routes.

**The consequence is counter-intuitive and it is the practical heart of this chapter:** a fast
route through a volatile corridor can cost more in total than a slower route through a stable
one. Optimising for speed is not the same as optimising for outcome, whereas most routing in
production today does not distinguish between the two because it is not computing either.

For a multi-hop route the exposures sum across the legs:

> **σ_total = Σ(σᵢ × √tᵢ)**

A three-hop corridor carries three separate exposure calculations added together, which is why
a corridor that looks cheap on headline spread can breach an exposure cap once the hops are
counted.

---

## 2.4 · The rate is not even one number before anyone adds a spread

This is the part we can speak to directly, because we measured it.

Lupine queries four independent public mid-market sources for AUD/SGD. On 3 August 2026, three
of the four were reachable and returned, at the same instant:

| Source | Rate | Source date |
|---|--:|---|
| open.er-api.com | 0.902119 | 2026-08-03 |
| jsdelivr currency-api | 0.901730 | 2026-08-02 |
| Frankfurter (ECB) | 0.901740 | 2026-07-31 |

A dispersion of **4.32 basis points** between sources that are all describing the same thing.

Two observations follow, and the second is the more interesting one.

First, the sources disagree. Not by much on this reading, however 4.32 bps is roughly a tenth of
what a competitive provider charges in total, and it sits *underneath* every spread anyone
quotes on top of it.

Second, **the three sources are not describing the same day.** Frankfurter's figure was three
days old at the moment of reading. So the phrase "the mid-market rate" resolves differently
depending on who you ask and how stale they are, before any provider has added a single basis
point of margin.

> **Provenance.** One observation, recorded by `scripts/spread_log.py` on 2026-08-03 and stored
> in `website/data/spread_log.jsonl`. The logger refuses to describe the dataset as citable
> below thirty observations. This is a demonstration of method, not yet a finding.

---

## 2.5 · Why this is not measured

The obvious question is why an industry moving trillions has no public decomposition of its own
pricing.

The answer is that **nobody in the chain is positioned to produce one.** A bank sees its own
leg. A correspondent sees the hop in front of it. A fintech sees inside its own network and,
reasonably, treats the composition of its spread as commercial information. The payer sees a
single quoted number at the start and a single credited amount at the end, whereas everything
between those two figures is distributed across parties that have no shared record and no
obligation to assemble one.

This is the same structural gap Chapter I described, seen from the cost side rather than the
latency side. It is not that the information is secret. It is that it is **never assembled**,
and the only party with an interest in assembling it is the one party with no access.

---

## 2.6 · What follows

The cost of non-determinism is real, it is structural, and its precise size is presently
unmeasured by anyone including us. That is an uncomfortable position for an essay to take, and
it is the correct one, whereas a fabricated decomposition would have read better and been worth
nothing.

**Chapter III** turns to why the problem has persisted: what SWIFT actually does and does not
do, why gpi delivered visibility without intelligence, and why the incumbents are structurally
unable to close the gap even where they can see it.

---

*Next: **III. Visibility Without Intelligence***

---

### Provenance summary

| Claim | Status | Source |
|---|---|---|
| Eight-component formula | cited | Study pack, P1-Ch4 — formula only, no values |
| Component basis-point split | **not established** | No published decomposition found |
| Wise take rate 0.70% / 0.77% | cited | Wise IPO prospectus 2021, pp. 77–78 |
| UK FPS nine-fold fee reduction | cited | Wise IPO prospectus 2021, pp. 49–51 |
| Hungary −14%, 17% → 82% instant | cited | Wise IPO prospectus 2021 |
| Exposure = σ√t | cited | Study pack, P1-Ch4 |
| σ_total across hops | cited | Study pack, P2-Ch4 |
| 4.32 bps source dispersion | **measured** | `spread_log.jsonl`, 2026-08-03, n=1 |
| Three-day staleness spread | **measured** | Same observation |
| "Nobody is positioned to measure it" | assertion | Argued, not demonstrated |

Full manifest: `docs/provenance.md`
