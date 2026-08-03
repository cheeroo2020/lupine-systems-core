# I. The Last Non-Deterministic Flow

*Deterministic Value — Chapter I of VII*
*Draft · Chirantan Gogoi · Lupine Systems*

---

On 27 July 2026, moving A$500,000 from Sydney to Singapore cost somewhere between 45 and 250 basis points, and took somewhere between two and a half hours and eleven days.

Not two different payments. **The same payment.** The range depends on a routing decision nobody computed — made by systems that never spoke to each other, on the basis of correspondent agreements signed years before the money existed.

If you asked the sending bank which of those outcomes you were about to get, it could not tell you. Not *would* not. **Could** not. The information required to answer does not exist in any single place, and no layer of the stack is responsible for assembling it.

That is a strange property for critical infrastructure to have in 2026. It is stranger still when you notice that every comparable flow in the economy fixed this decades ago.

---

## 1.1 · Four flows that stopped guessing

The history of modern infrastructure is largely the history of things becoming predictable.

**Physical goods, 1956.** Before containerisation, loading a cargo ship was manual, bespoke, and slow — days in port, roughly $5.86 per ton. Arrival dates were estimates. Malcom McLean's insight was not a better crane; it was a *standard unit*. Once every box was the same box, the entire chain could be planned. Cost fell toward $0.16 per ton. More importantly, **schedules became schedules** rather than hopes.

**Data, 1970s–80s.** Early databases lost data on power failure as a matter of routine. A crash mid-write left records half-updated with no way to tell which. The fix was the transaction: a set of guarantees under which a write either **fully commits or fully rolls back**, with nothing in between. Atomicity turned storage from a probabilistic activity into a deterministic one.

**Communications, 1974.** Raw packet networks drop packets, reorder them, and duplicate them. TCP did not eliminate that — it made it *irrelevant to the application*. Sequence numbers, acknowledgements and retransmission moved unreliability beneath a layer that guarantees ordered delivery. The network stayed messy. The interface became certain.

**Compute, 2006.** Before EC2 entered public beta, capacity meant procurement: quotes, purchase orders, racking, weeks of lead time, and a guess about demand. After, it meant an API call and a service level agreement. The resource did not change. **The predictability of obtaining it did.**

Four different domains, four different decades, four different technical mechanisms. One shared pattern:

> A flow stops being managed reactively and starts being **computed in advance** — and the guarantee is moved into the infrastructure rather than left with the user.

---

## 1.2 · The holdout

Value did not get this.

A cross-border payment in 2026 still behaves the way shipping behaved in 1950 and storage behaved in 1975. It is handed off between institutions that do not share operating hours, liquidity positions, compliance interpretations, or message formats. Each hop makes a local decision with local information. Nobody holds the whole path.

The specific failures are well documented and have not meaningfully changed in twenty years:

- **Routing is static.** The path follows correspondent relationships negotiated years earlier and pre-funded accounts held for treasury reasons. It is not computed per payment, and it does not respond to today's conditions.
- **Liquidity is invisible.** Nostro accounts are pre-funded pools. When one is exhausted, payments do not fail — they **queue**, silently, until it is topped up. The payer is not told this is happening because the payer's bank does not know either.
- **Compliance re-runs at every hop, independently.** A payment screened clean at origin can be flagged by the third intermediary for a reason no one predicted, because no two institutions interpret the rules identically.
- **Settlement windows do not overlap.** AU RITS runs 08:00–18:00 AEST. EU TARGET2 runs 17:00–02:00. US Fedwire runs 21:00–05:30. There is no hour of the day when all three are open, and a payment that misses its window waits.

None of this is incompetence. Each institution is behaving rationally within its own boundary. **The dysfunction is structural** — it lives in the absence of a layer that sees across the boundaries, and no participant is incentivised to build one.

---

## 1.3 · What determinism actually means

The word needs to be precise, because it is doing load-bearing work for the rest of this essay.

**Deterministic does not mean fast.** It does not mean cheap, and it does not mean guaranteed to succeed.

> **Deterministic means: given the same inputs, you get the same output — and you know the output before you commit.**

No randomness. No human judgment inserted mid-flow. No two identical payments taking different paths for reasons that cannot afterwards be reconstructed.

Legacy correspondent banking fails this test in the most basic possible way. Send the same A$500,000 twice, an hour apart, and it may route differently, arrive days apart, and cost materially different amounts — and no one involved can tell you why, because the decision was never made in one place to begin with.

A deterministic system does not promise the payment will be fast. It promises that **whatever is going to happen is knowable in advance**, and that the reasoning is reconstructable afterwards. Those are different guarantees, and the second is the one that has been missing entirely.

---

## 1.4 · The measurement

The cost of non-determinism is measurable, and this is the number that motivates everything that follows.

On the Australia–Singapore corridor:

| Outcome | Elapsed |
|---|---|
| Best observed | 2.5 hours |
| Median | 28–36 hours |
| P95 | 3–5 days |
| Worst observed | 7–11 days |

**Best to worst: a factor of roughly 106×.**

> **Provenance.** These bands are cited from an internal research document for the
> three-leg corridor **AU → SG → DE**, not for AU → SG alone, and have not been
> independently verified. See `docs/provenance.md`.

Compare that to any other infrastructure you depend on. A cloud API call that took 106× its median latency would be a Sev-1 incident. A container ship arriving 106× late would end a shipping line. In cross-border value movement, that spread is not an incident. **It is the normal operating envelope**, and it is not disclosed to the payer.

The cost side is similar. The rate you are quoted is one number. The rate you actually pay is the sum of eight components — interbank spot, spread, forward points, volatility premium, liquidity premium, corridor cost, delay premium, and a compliance risk buffer. The formula is cited; the values are not. No basis-point split for this corridor has been measured, and any figure given for one here would be invented.

> **Six of the eight components are not disclosed to the payer at any point — so the payer cannot evaluate the transaction they are agreeing to, whatever the figure turns out to be.**

And one of those hidden components is the price of delay itself — which means unpredictability is not merely inconvenient. It is directly, quantifiably expensive.

---

## 1.5 · This is not an essay about fees

It would be easy to read the preceding section as a complaint about bank margins. It is not, and the distinction matters.

Several excellent companies have already attacked the fee problem. Wise spent a decade and sixty-three licences building direct integrations into local payment systems, and cut the cost of a UK transfer nine-fold in the process. Remitly built a network spanning 1,700 corridors. Adyen collapsed a fragmented card value chain into one platform with real-time failover across six data centres. These are serious pieces of infrastructure and the fee problem is, slowly, being solved.

**None of them solved the determinism problem**, and structurally none of them can.

Each optimises routing *inside its own network*. Wise cannot recommend Airwallex. Adyen cannot route you off Adyen. Remitly cannot tell you a competitor's corridor would have been better today. Their optimisation is genuine and it is also captive — bounded by the network they own, which is precisely the asset that makes them valuable.

More fundamentally: none of them can hand you a proof. When a payment is delayed, you receive an explanation. You cannot independently verify the route that was chosen, the alternatives that existed, or the reasoning that discarded them. You are asked to trust the record of the party whose performance the record describes.

That is the gap this essay is about. Not *what does it cost* — but:

> **Can the decision be computed in advance, and can the reasoning be proved afterwards by someone who does not trust you?**

---

## 1.6 · What follows

The remainder of this essay argues that value movement is now at the point shipping reached in 1955, storage reached in 1978, and compute reached in 2005 (EC2 beta 2006, general availability 2008) — a domain where the dysfunction is fully understood, the enabling components have quietly arrived, and nobody has yet assembled them.

The enabling components exist. ISO 20022 gives structured, schema-validated payment data where MT103 gave ambiguous free text. Real-time FX is available to anyone with an HTTP client. Cryptographic evidence chains are decades-old technology, cheap to run. What has not existed is a layer that treats a payment as a *decision to be computed* rather than an *instruction to be forwarded*.

**Chapter II** measures the cost of non-determinism precisely — the eight FX components, the non-linear relationship between delay and exposure, and why a faster route can be the more expensive one.

**Chapter III** examines why the problem has persisted: what SWIFT actually does and does not do, why gpi delivered visibility without intelligence, and why the incumbents are structurally unable to solve it.

**Chapters IV through VI** describe what a deterministic layer requires — computed routing, enforced execution, verifiable evidence — and then, in Chapter VI, an itemised account of how much of it currently runs, including everything that does not.

That last chapter is deliberate. An argument for verifiability that is vague about its own maturity is self-refuting.

---

*Next: **II. What Non-Determinism Costs***
