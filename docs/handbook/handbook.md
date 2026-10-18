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
- **Part III — Study record**, organised by textbook part. Each sitting is recorded once it is checked: your answers, mistakes and own-words explanations.
- **Part IV — Experiments.** A one-page summary of each practical experiment. The full record and the raw
  measurements live in `experiments/`, the only authoritative copy.
- **Part V — Quick reference.** Formulas, terms, safety rules and troubleshooting, for looking things up fast.
- **Appendices.** Personal planning framework, sources, correction history, edition history, and how to maintain this file.

The course text itself is the textbook in `docs/textbook/` (see Part I, *The course text*).
Three other places hold material this handbook draws on: `experiments/` (records and raw data),
`research/` (reading notes, problem observations, conversation summaries) and `docs/architecture.md`
(what the code really does).

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

| Period | Focus | Textbook | Evidence required to move forward |
|---|---|---|---|
| 19 Oct – Dec 2026 | Electrical fundamentals, measurement, basic programming, an overview of Tasmania's energy and data-centre systems. Rail's existing rules alongside. | Parts 01, 02 (reading only) and 03; feedback loops 06-03 to 06-07; Tasmania 07-03 to 07-10; Rail rules 08-28 to 08-30 | Explain voltage, current, power and energy; do basic calculations; explain a control loop; distinguish an acknowledgement from an observed result. |
| Jan – Mar 2027 | Build one safe, low-voltage instrumented device. Sensors, uncertainty, actuators, response time. Connect Lupine to it progressively. | Part 04; Part 05; build Part 02's temperature logger (02-25, 02-26); gates G1–G2 (08-05) | Repeatable measurements, documented limitations, and a demonstration of a command, an acknowledgement and a physical response. |
| Apr – Jun 2027 | Make the prototype handle communication loss, stale readings, restart and reconciliation. Learn an industrial protocol when the device needs one. | Part 06 from 06-08; Modbus 06-11 to 06-13 and 08-22; gates G3–G4 | Recorded physical experiments showing what happens during failures. You can explain and modify the important code yourself. |
| Jul – Dec 2027 | Choose one narrow energy infrastructure problem, informed by engineering conversations and existing solutions. Adapt the prototype to test it. | Part 07 in full, especially the problem brief (07-28, 07-29); gate G5 | A specific user, a recurring problem, an explanation of current approaches, and a measurable improvement worth testing. |
| 2028 | Seek a supervised external trial with a suitable engineering partner. Build the reliability, integration and documentation that setting needs. | Bench to field (08-35); product test (08-36) | Results from an agreed trial against a meaningful baseline, with limitations and responsibilities clearly defined. |
| 2029 onward | Pursue a commercial product if trial results and customer commitment support it. Keep deepening the chosen specialty. | 08-36; return to any part as the specialty demands | Evidence that users benefit, someone will pay, and the product can be delivered and supported responsibly. |

## The course text

**One textbook:** *Energy Infrastructure: The Visual Engineering Handbook*, complete eight-part edition, 295 pages, dated 16–17 October 2026, prepared with ChatGPT. File: `docs/textbook/energy-infrastructure-visual-handbook-8-part-2026-10-17.pdf`. Cite pages by their printed label: **01-08** means Part 01, page 8.

**Review status.** [VERIFIED] on 17 October 2026, scope: calculations and code. About 200 worked examples and answers were recalculated with no errors found, and all seven programs produce the outputs the book states. The device facts match manufacturer documentation. Not established: no physical testing and no professional engineering review, which the book says itself.

**Three conditions of use:**

1. It is the only course text. It replaces the earlier 96-lesson survey (now in `docs/textbook/superseded/`) and the chat-lesson plan in edition 0.1 of this handbook. This handbook stays the record of what you did, not a second textbook.
2. Learn the maths it uses but does not teach, before the parts that need it (below).
3. It is never the authority for real equipment. Datasheets, standards and qualified engineers are. Part 07's project figures are a dated snapshot: recheck before quoting.

### Maths to learn first

| Before | Maths | Where it is used |
|---|---|---|
| Part 03 | Sine and cosine, degrees and radians, √2; complex numbers (j, magnitude and angle) | RMS and phase (03-04, 03-05), impedance (03-07), the power triangle (03-08) |
| 06-03 | Rates and accumulation: slope as a derivative, area as an integral (`dv/dt`, `∫e dt`) | Feedback and PID (06-04 to 06-07); also 02-07, 02-08 |
| Part 04 | Exponentials and natural logarithms (`exp(-t/τ)`, `ln`) | Time constants (04-11), heat exchangers (04-20) |

Each supplement is a short lesson from Claude, recorded in Part III like any other sitting.

### Names in the textbook and in Rail's code

| Textbook | Rail code (`src/rail_lite/`) |
|---|---|
| observed_match (06-16) / completed (08-13) | `completed` |
| observed_mismatch / mismatched | `mismatched` |
| not_executed / failed | `failed` |
| uncertain | `uncertain` |
| fenced_no_execution receipt (06-30) | `Receipt.fenced_no_execution` |
| bare "not found" stays uncertain (06-19) | `Receipt.not_found` gives `uncertain` |
| device epoch or boot identity (06-30, 08-12) | `Instruction.session`, `Observation.session` |
| resource (08-12) | `Instruction.resource`, `Observation.resource` |

### Known issues in the textbook

| Page | Issue | What to do |
|---|---|---|
| 01-02 | The series map shows an older ten-part plan and says the other parts are not yet delivered | Ignore it. The order is the eight parts on page 003 |
| Last page of each part | "N planned parts remain" | Leftover from merging; all eight parts are present |
| 02-23 | The logger's −55 to 125 °C check accepts 85 °C, which the sensor reports at power-on before its first conversion [ASSUMED: DS18B20 datasheet power-on value; confirm when building] | Treat an 85 °C first reading as suspect when you build it |
| 04-32 | The table lists a 160 s row that the program does not print | The value, 32.1139 °C, is correct; it comes from the equation |
| Parts 06 and 08 | Two sets of names for the same verdicts | Use the name table above |
| 08-31 | Proposes a different repository layout (`src/energy/`, `docs/energy/`) | Not adopted. The layout is in `CLAUDE.md` |
| 08-33, 08-34 | Its own first week and month-by-month timeline | Not used. Part II and the timeline above are the plan |
| Part 07 | Project figures are a 17 October 2026 snapshot. A web check did not confirm three of them: 84 MW critical IT, the "non-firm" Wesley Vale wording, and the 16 October Marinus update | Recheck the dated source before quoting |

## How we work

Every study sitting follows the same five steps:

1. **Explain.** Read the textbook pages for the sitting. When a page is too compressed, ask Claude for a fuller explanation and extra practice problems.
2. **Demonstrate.** Follow the worked examples, every step shown.
3. **Attempt.** Do the practice problems. Predict first, then calculate or measure.
4. **Check.** Explain your result in your own words. Mistakes are investigated, not skipped.
5. **Record.** The sitting goes into Part III, including what you got wrong.

Complexity increases only when you can explain the current step. One sitting at a time.

## Safety rules

These hold until a later, explicit decision changes them. Hardware purchases are postponed for now.

- **5 V USB power only.** No other supply until we decide together.
- **No mains work, ever.** In Australia, work on mains (230 V) wiring must be done by a licensed electrician. [ASSUMED] Check the Tasmanian licensing rules with CBOS; this is an open source to confirm.
- **No loose lithium cells.** Real energy storage comes later, and only as a sealed product with its own protection electronics.
- **Nothing left powered and unattended.**

## What Lupine is today

Status as of 17 October 2026, tested at repository commit `7893062`. Lupine was written for cross-border payments. This table records what carries over to energy.

| Piece | What it really does | Label | Use for energy |
|---|---|---|---|
| Rail outcome rules (`src/rail_lite/outcome.py`, `executor.py`) | Turns evidence (a receipt and a reading) into one of four verdicts, after checking the evidence is about the right instruction, resource and device session; blocks unsafe retries | [VERIFIED] by 36 automated tests, **in simulation only** | Yes, directly. Missing: units on targets, real communication, timeouts, saving state to disk, a real clock |
| Cloked (`src/cloked_lite/logger.py`) | A SHA-256 hash chain, held in memory | [VERIFIED] 16 Oct 2026 by test: a forger who recomputes every later hash still passes `verify_chain()` | Partly. Needs its final hash stored where a forger can't reach it, then signatures |
| Aiva (`src/aiva_lite/`) | A weighted sum of three scores | Runs; its inputs are [ASSUMED] (unchecked provider figures, invented reliability values) | The pattern only. Engineering limits must be pass/fail checks *before* any scoring |
| FX feed, watcher, website, API | Payment-specific | FX values [MEASURED]; provider costs [ASSUMED] | No. They keep running without attention |

The simulated device for Rail's rules is `scripts/rail_uncertainty_demo.py`. It is a pretend battery controller and is [SIMULATED]. It models no real device.

Full module-by-module detail, the dependency map and the automation inventory are in `docs/architecture.md`.

\pagebreak

# Part II — Weekly plans and reviews

## Week 1 — 19 to 25 October 2026

**Theme:** Textbook Part 01, *Electricity You Can Measure*: one 5 V circuit, understood completely. Then the shape of Tasmania's energy system.

**Rule for this week:** sittings 1–4 are in order, and each waits until you can explain the one before it. Sessions 5–7 don't depend on them and can happen in any order.

| # | Suggested day | Time | Session | Done when |
|---|---|---|---|---|
| 1 | Mon 19 | 1.5 h | **Part 01, sitting 1:** pages 01-03 to 01-10. The physical picture; voltage, current and resistance. | You can explain 01-04 to 01-07 aloud without looking |
| 2 | Tue 20 | 1.5 h | **Part 01, sitting 2:** pages 01-11 to 01-15. Series and parallel; power; energy. | You can redo the 01-14 example from a blank page |
| 3 | Wed 21 | 1.5 h | **Part 01, sitting 3:** pages 01-16 to 01-21. Measuring current; bounds; zero, missing and stale. Then Claude shows the matching rule in `src/rail_lite/outcome.py`. | You can say why a missing reading is not zero, in the circuit and in the code |
| 4 | Thu 22 | 1.5 h | **Part 01, sitting 4:** the 8 practice problems (01-22). Send your answers; then compare with 01-23. | Answers checked; mistakes and corrections recorded in Part III |
| 5 | Fri 23 | 1.5 h | **Tasmania, part 1:** textbook 07-03 to 07-08. Orientation, organisations, hydro, Basslink and Marinus. | Four facts recorded, each with source, date and label |
| 6 | Sat 24 | 1.5 h + 1 h | **Programming 1:** set up Python and reproduce practice problems 1 and 3 in a few lines. **Industry list:** five people or organisations from 07-04 and 07-26; draft a four-sentence introduction (not sent). | Script matches 01-23; list and draft added here |
| 7 | Sun 25 | 1 h | **Weekly review:** what you can explain, what is shaky; update this handbook; produce edition 0.2 | Edition 0.2 exists |

Total ≈ 11 hours. The panel-heater exercise from the 16 October chat lesson is optional extra practice; Part 01 covers the same ground.

### Review — Week 1

*To be completed on Sunday 25 October 2026.*

\pagebreak

# Part III — Study record

One section per textbook part, one entry per sitting. The textbook holds the explanations; this part holds what *you* did with them.

## Textbook Part 01 — Electricity You Can Measure

### Sittings 1–4 (pages 01-03 to 01-24)

::: pending
Starts Monday 19 October 2026. Each sitting is recorded once you have explained it back and the practice answers (01-22) are checked: your answers, mistakes and corrections, your own-words explanation, anything the textbook didn't make clear, and new glossary terms. The earlier chat lesson of 16 October (the kettle: voltage, current, power and energy) covered the same ground and is superseded by these sittings.
:::

\pagebreak

# Part IV — Experiments

No experiments yet. Hardware is postponed until the fundamentals are in place.

## Where experiment records live

Each experiment has its own folder, `experiments/E00N-short-name/`. The folder holds the full record and the **only authoritative copy of the raw measurements**. This Part gives each experiment a one-page summary and links to its folder by ID. It never copies raw data.

The record template is `experiments/TEMPLATE.md`. It covers:

1. **Question**, and **equipment and setup**, with model numbers.
2. **Prediction**, written *before* measuring and never revised.
3. **Procedure**, and **measurements** with units, instrument, date and time.
4. **Calculations and uncertainty.**
5. **Failures and limitations.**
6. **What this establishes**, labelled, with the scope of any verification, and **what remains unknown.**
7. **Code files and the exact repository commit tested.**
8. **Your own explanation.**

The rules, including "raw data is never edited", are in `experiments/README.md`.

\pagebreak

# Part V — Quick reference

## Formulas

*Added as each textbook part is completed.* The textbook's own formula pages: 01-24, 02-30, 03-33, 04-36, 05-37, 06-37 and 07-37.

## Terms

| Term | Meaning |
|---|---|
| Aiva | Lupine's decision layer. Today: a weighted score over options. |
| Rail | Lupine's execution layer. Sends an instruction, then decides what the evidence supports. |
| Cloked | Lupine's evidence layer: a hash chain recording what happened. The spelling is deliberate. |
| Receipt | What the other side says about an instruction: accepted, rejected, no record of it, or a guarantee that it can never run ("fenced"). |
| Session | The device's current power-on period. Evidence from a different session can't confirm an instruction. |
| Reading | A measured value from a sensor, with the time it was taken. |
| Tolerance | How far a reading may be from the target and still count as meeting it. |
| Reconciliation | Gathering fresh evidence to resolve an uncertain outcome before deciding anything else. |

The textbook's glossaries: 02-31, 03-34, 04-37, 05-38 and 06-38.

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
| *Energy Infrastructure: The Visual Engineering Handbook*, eight-part edition (`docs/textbook/`) | The course text; Part I, *The course text* | 17 Oct 2026 |
| Hydro Tasmania, Cethana pumped hydro project page | Checking Part 07's 750 MW / 20 h figure (confirmed) | 17 Oct 2026 |
| Pulse Tasmania; W.Media; DatacenterDynamics (news on Firmus sites) | Checking Part 07's Firmus figures: 104 MW Aurora supply and the 26 MW Wesley Vale initial connection confirmed; 84 MW not found | 17 Oct 2026 |
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
- **Textbook:** `docs/textbook/`. Read-only course text; its known issues are listed in Part I.
- **Build:** `python scripts/build_handbook.py`. It reads `version` and `edition_date` from the top of the master. It needs one library, installed once with `pip install -r docs/handbook/requirements.txt`.
- **Editions:** written to `docs/handbook/editions/`. The script refuses to overwrite an existing edition, so earlier PDFs are always preserved. Raise the version number for each new edition.
- **Logo:** the cover uses `website/assets/brand/lupine-logo.png`, derived from the approved original in the same folder.
- **Syntax:** `#` for a part, `##` and `###` for sections, `-` for bullets, `|` for tables, triple backticks for equations. A `::: yours` box holds your own words, `::: note` a side note, `::: pending` work in progress, and `\pagebreak` forces a new page. Labels in square brackets, such as `[MEASURED]`, become coloured tags.
