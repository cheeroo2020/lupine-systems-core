---
title: Lupine Energy Engineering Handbook
subtitle: A learning record and project log
owner: Chirantan (Chris) Gogoi · Hobart, Tasmania
version: 0.1
edition_date: 2026-10-16
---

<!--
EDITABLE MASTER. This file is the source of truth for the handbook.
Build a PDF edition:   python scripts/build_handbook.py
Editions are written to docs/handbook/editions/ and are never overwritten.
Syntax guide: Appendix E.
-->

# How to use this handbook

This handbook is the written memory of the work. It should let you return after months away and pick up where you left off, without rereading any conversation.

## What it contains

- **Part I — Direction.** Your goals, the timeline, how we work, and what Lupine actually is today.
- **Part II — Weekly plans and reviews.** One page per week: the plan, then what actually happened.
- **Part III — Lessons**, organised by topic. Each lesson is recorded only after it is complete, including your answers and mistakes.
- **Part IV — Experiments.** Each practical experiment, from question to conclusion.
- **Part V — Quick reference.** Formulas, terms, safety rules and troubleshooting, for looking things up fast.
- **Appendices.** Personal planning framework, sources, correction history, edition history, and how to maintain this file.

## Two voices, kept apart

Explanations written by Claude are ordinary text. Your own words always appear in a shaded box headed **In my own words — Chris**. The first one is your goals statement in Part I. A box contains only what you wrote yourself, unedited except for spelling. If something in it is wrong, it stays, and the correction is written beside it.

Keeping the two apart matters. It shows what you can explain unaided. That is the evidence each stage of the timeline asks for.

## Claim labels

Every factual claim that matters carries one of four labels. When the label is **[VERIFIED]**, the text must also say what was checked, how, and the limits of the check.

| Label | Meaning | What must be recorded with it |
|---|---|---|
| [ASSUMED] | Taken as true without our own check: a rating plate, a typical value, a published figure | The source, and the date it was read |
| [SIMULATED] | Produced by software modelling a system. True only inside the model's assumptions | The model, its assumptions, the code file and commit |
| [MEASURED] | Observed with an instrument we used | Instrument, method, date, and the uncertainty |
| [VERIFIED] | Checked against an independent method or source | What was checked, how, and the **scope** of the check |

Two examples of scope:

- "Rail handles a lost reply correctly" is **[VERIFIED] by automated tests, in simulation only**. It says nothing about real equipment.
- "The sensor read 0.52 A" is **[MEASURED]**. It becomes **[VERIFIED] to ±2%** only after a second, independent instrument agrees within 2%.

\pagebreak

# Part I — Direction

## Goals

These are your words, recorded as stated on 16 October 2026.

::: yours
My direction is energy infrastructure, with Lupine as the project through which I learn and build. I want a long-term technical career and eventually a venture connected to Tasmania's energy systems and AI infrastructure.

My goal is to build Lupine into an energy technology company, starting in Tasmania and potentially serving problems elsewhere. I also want to develop the technical expertise to understand, design and troubleshoot what we build.

I am serious about making this my life's work. I am committing to the field and to developing expertise; the exact product must emerge from evidence and experience.
:::

What this means in practice:

- **Starting point.** An industrial and production engineering background. A beginner in electrical engineering, computing and software. Based in Hobart. About 10–12 hours a week.
- **What to understand.** The physical system first: generation, the Tasmanian grid, power conversion, batteries, controls, sensors, communications, and how these connect to data centres, computing and cooling. Then the software that controls them.
- **The world to enter.** Firmus, Hydro Tasmania, TasNetworks and UTAS are named as relevant. Industry conversations start within the first three months and continue throughout.
- **The product stays open.** Reuse Lupine where it meets real engineering requirements and change it where it doesn't. Lupine's architecture alone does not establish a market. Commercial uncertainty stays explicit while the learning continues.
- **Not this.** No steering towards finance, billing, reporting or general operations roles.

## Timeline and evidence gates

Dates are planning targets. You move to the next period when you can show its evidence, not when the calendar says so.

| Period | Focus | Evidence required to move forward |
|---|---|---|
| 19 Oct – Dec 2026 | Electrical fundamentals, measurement, basic programming, an overview of Tasmania's energy and data-centre systems. Rail's existing rules alongside. | Explain voltage, current, power and energy; do basic calculations; explain a control loop; distinguish an acknowledgement from an observed result. |
| Jan – Mar 2027 | Build one safe, low-voltage instrumented device. Sensors, uncertainty, actuators, response time. Connect Lupine to it progressively. | Repeatable measurements, documented limitations, and a demonstration of a command, an acknowledgement and a physical response. |
| Apr – Jun 2027 | Make the prototype handle communication loss, stale readings, restart and reconciliation. Learn an industrial protocol when the device needs one. | Recorded physical experiments showing what happens during failures. You can explain and modify the important code yourself. |
| Jul – Dec 2027 | Choose one narrow energy infrastructure problem, informed by engineering conversations and existing solutions. Adapt the prototype to test it. | A specific user, a recurring problem, an explanation of current approaches, and a measurable improvement worth testing. |
| 2028 | Seek a supervised external trial with a suitable engineering partner. Build the reliability, integration and documentation that setting needs. | Results from an agreed trial against a meaningful baseline, with limitations and responsibilities clearly defined. |
| 2029 onward | Pursue a commercial product if trial results and customer commitment support it. Keep deepening the chosen specialty. | Evidence that users benefit, someone will pay, and the product can be delivered and supported responsibly. |

## How we work

Every lesson follows the same five steps:

1. **Explain.** The concept, the units, the equation, and the assumptions behind it.
2. **Demonstrate.** One worked example, every step shown.
3. **Attempt.** You do one exercise. Predict first, then calculate or measure.
4. **Check.** You explain your result in your own words. Mistakes are investigated, not skipped.
5. **Record.** The lesson goes into Part III, including what you got wrong.

Complexity increases only when you can explain the current step. One lesson at a time.

## Safety rules

These hold until a later, explicit decision changes them. Hardware purchases are postponed for now.

- **5 V USB power only.** No other supply until we decide together.
- **No mains work, ever.** In Australia, work on mains (230 V) wiring must be done by a licensed electrician. [ASSUMED] Check the Tasmanian licensing rules with CBOS; this is an open source to confirm.
- **No loose lithium cells.** Real energy storage comes later, and only as a sealed product with its own protection electronics.
- **Nothing left powered and unattended.**

## What Lupine is today

Status as of 16 October 2026, tested at repository commit `e5582dd`. Lupine was written for cross-border payments. This table records what carries over to energy.

| Piece | What it really does | Label | Use for energy |
|---|---|---|---|
| Rail outcome rules (`src/rail_lite/outcome.py`, `executor.py`) | Turns evidence (a receipt and a reading) into one of four verdicts; blocks unsafe retries | [VERIFIED] by 30 automated tests, **in simulation only** | Yes, directly. Missing: real communication, timeouts, saving state to disk, a real clock |
| Cloked (`src/cloked_lite/logger.py`) | A SHA-256 hash chain, held in memory | [VERIFIED] 16 Oct 2026 by test: a forger who recomputes every later hash still passes `verify_chain()` | Partly. Needs its final hash stored where a forger can't reach it, then signatures |
| Aiva (`src/aiva_lite/`) | A weighted sum of three scores | Runs; its inputs are [ASSUMED] (unchecked provider figures, invented reliability values) | The pattern only. Engineering limits must be pass/fail checks *before* any scoring |
| FX feed, watcher, website, API | Payment-specific | FX values [MEASURED]; provider costs [ASSUMED] | No. They keep running without attention |

The simulated device for Rail's rules is `scripts/rail_uncertainty_demo.py`. It is a pretend battery controller and is [SIMULATED]. It models no real device.

\pagebreak

# Part II — Weekly plans and reviews

## Week 1 — 19 to 25 October 2026

**Theme:** what electricity is, in numbers you can calculate; and the shape of Tasmania's energy system.

**Rule for this week:** a session that depends on a lesson waits until that lesson's exercise has been checked. Sessions 4–6 don't depend on the lessons and can happen in any order.

| # | Suggested day | Time | Session | Done when |
|---|---|---|---|---|
| 1 | Mon 19 | 1.5 h | **Lesson 1:** voltage, current, power and energy. One worked example, one exercise. | Your answer has been checked |
| 2 | Tue 20 | 1.5 h | **Lesson 2:** the kettle as a system. Instruction, controller, measurement and evidence, then the matching Lupine code. | You can point to all four in the kettle and in `outcome.py` |
| 3 | Wed 21 | 1.5 h | **Lesson 3:** resistance and Ohm's law; why wires get warm | Exercise checked |
| 4 | Thu 22 | 2 h | **Tasmania, part 1 (reading):** Hydro Tasmania, TasNetworks, Basslink, AEMO's Tasmania region, and what Firmus says publicly that it builds | Four facts recorded, each with source, date and label |
| 5 | Fri 23 | 1.5 h | **Programming 1:** set up Python on your own computer and reproduce Lesson 1's worked example in five lines | Your script runs and matches the hand calculation |
| 6 | Sat 24 | 1 h | **Industry conversations, part 1:** list five people or organisations to approach; draft a four-sentence introduction (not sent yet) | List and draft added here |
| 7 | Sun 25 | 1 h | **Weekly review:** what you can explain, what is shaky; update this handbook; produce edition 0.2 | Edition 0.2 exists |

Total ≈ 10 hours.

### Review — Week 1

*To be completed on Sunday 25 October 2026.*

\pagebreak

# Part III — Lessons

## Topic A — Electrical fundamentals

### Lesson 1 — Voltage, current, power and energy

::: pending
In progress, started 16 October 2026. Recorded here once the exercise has been answered and checked: the explanation, units, equations and assumptions, the worked example, your answer and any corrections, your own-words explanation, sources and new glossary terms.
:::

\pagebreak

# Part IV — Experiments

No experiments yet. Hardware is postponed until the fundamentals are in place.

## Record template

Every experiment is recorded under these headings:

1. **Question.** What exactly are we trying to find out?
2. **Equipment and setup.** Every item, with model numbers, and a diagram.
3. **Prediction.** Written down *before* measuring, with the reasoning.
4. **Procedure.** Steps detailed enough that someone else could repeat them.
5. **Measurements.** Raw values, units, instrument, date and time.
6. **Calculations and uncertainty.** Working shown, and how sure we are.
7. **Failures and limitations.** What went wrong, and what the setup can't show.
8. **What this establishes.** Labelled, with the scope of any verification.
9. **What remains unknown.**
10. **Code and commit.** The files involved and the exact repository commit tested.

\pagebreak

# Part V — Quick reference

## Formulas

*Added as each lesson is completed.*

## Terms

| Term | Meaning |
|---|---|
| Aiva | Lupine's decision layer. Today: a weighted score over options. |
| Rail | Lupine's execution layer. Sends an instruction, then decides what the evidence supports. |
| Cloked | Lupine's evidence layer: a hash chain recording what happened. The spelling is deliberate. |
| Receipt | What the other side says about an instruction: accepted, rejected, or no record of it. |
| Reading | A measured value from a sensor, with the time it was taken. |
| Tolerance | How far a reading may be from the target and still count as meeting it. |
| Reconciliation | Gathering fresh evidence to resolve an uncertain outcome before deciding anything else. |

## Safety rules

See Part I. Short form: 5 V USB only, no mains, no loose lithium, nothing unattended.

## Troubleshooting

*Added as problems are met and solved.*

\pagebreak

# Appendices

## Appendix A — Personal planning framework

This is a personal reflection framework you asked for. It is **not evidence**, and never a reason to postpone useful work or to expect an outcome. Engineering decisions are made on engineering evidence.

**System used.** Western astrology, tropical zodiac. Houses use the whole-sign system, cross-checked against Placidus. Planetary positions come from the Swiss Ephemeris (`pyswisseph`, built-in Moshier ephemeris).

**Birth data.** Supplied by you, and [ASSUMED] accurate. It is kept out of this file because the repository is public.

**Verification (16 Oct 2026).**

- Positions were computed from the supplied birth data.
- The rising sign was cross-checked by computing sunrise independently for the birthplace. The birth time falls shortly before sunrise, which matches the computed Ascendant.
- The rising sign stays the same for a birth-time error of up to about ±1 hour.
- Scope of the check: the astronomical positions only. Interpretations are not verifiable and carry no label.

**Rising sign:** Libra. In whole-sign houses, Leo is the 11th house, Virgo the 12th and Libra the 1st.

| Period (Jupiter's sign) | Your planning theme | House overlay (whole-sign) |
|---|---|---|
| 30 Jun 2026 – 26 Jul 2027 (Leo) | Developing confidence, sharing progress, finding technical mentors | 11th: networks, groups, mentors |
| 26 Jul 2027 – 24 Aug 2028 (Virgo) | Craftsmanship, systematic testing and refinement | 12th: quiet, behind-the-scenes work |
| from 24 Aug 2028 (Libra) | Partnerships, and presenting work publicly when the evidence supports it | 1st: self and public presence. Jupiter returns to its birth position around 26 Aug 2028 |

Ingress dates are computed from the ephemeris, not looked up. Saturn is in Aries from 14 Feb 2026 to 13 Apr 2028, which is your whole-sign 7th house. Traditionally that is read as a period for seriousness about commitments with others.

## Appendix B — Sources

| Source | Used for | Read |
|---|---|---|
| Swiss Ephemeris via `pyswisseph` (Moshier mode) | Appendix A positions and dates | 16 Oct 2026 |
| Your own statements, 16 Oct 2026 | Goals, timeline, working method | 16 Oct 2026 |

## Appendix C — Correction history

Errors found in this handbook, with the date found and what changed. Nothing is deleted silently.

| Date | Section | Was | Corrected to | How found |
|---|---|---|---|---|
| — | — | No corrections yet | — | — |

Corrections to Lupine's published figures before this handbook began are in `docs/provenance.md`.

## Appendix D — Edition history

| Edition | Date | Contents |
|---|---|---|
| 0.1 | 16 Oct 2026 | First edition: goals, timeline, method, safety rules, Lupine status, Week 1 plan, planning framework |

## Appendix E — Maintaining this handbook

- **Master:** `docs/handbook/handbook.md`. Edit this file; never edit a PDF.
- **Build:** `python scripts/build_handbook.py`. It reads `version` and `edition_date` from the top of the master. It needs one library, installed once with `pip install -r docs/handbook/requirements.txt`.
- **Editions:** written to `docs/handbook/editions/`. The script refuses to overwrite an existing edition, so earlier PDFs are always preserved. Raise the version number for each new edition.
- **Syntax:** `#` for a part, `##` and `###` for sections, `-` for bullets, `|` for tables, triple backticks for equations. A `::: yours` box holds your own words, `::: note` a side note, `::: pending` work in progress, and `\pagebreak` forces a new page. Labels in square brackets, such as `[MEASURED]`, become coloured tags.
