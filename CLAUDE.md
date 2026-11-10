# CLAUDE.md — Lupine

> Canonical context for AI coding agents in this repo. Reset on 10 November 2026.

---

## 1. Direction

Lupine is **Chris (Chirantan Gogoi)'s interactive learning website, in Hobart, which grows into a live
technical portfolio.** The goal is to understand:

1. how **AEMO** runs the National Electricity Market (NEM);
2. how **TasNetworks** plans and operates Tasmania's transmission and distribution networks;
3. **where their responsibilities meet.**

A job application may benefit from the work, but it does not drive the schedule. Don't steer toward
finance, billing, reporting or general operations roles.

Chris has an industrial and production engineering background, is a beginner in electrical engineering
and software, and studies about 10–12 hours a week.

## 2. Sources

Two core sources, Chris's own copies:

| Source | File | How to cite |
|---|---|---|
| AEMO, *NEM Foundations* eLearning, 2026 | `docs/NEM Foundations 2026.pdf` | Module, lesson and PDF page (the course has no printed page numbers), e.g. "NEM M3 L2, PDF p. 84" |
| TasNetworks, *Annual Planning Report 2026* | `docs/TasNetworks-APR-2026_compressed.pdf` | Printed page (PDF page = printed + 2), plus table or figure, e.g. "APR p. 63, Table 4-1" |

- **Read their actual contents.** Never cite from memory.
- **Never reproduce or publish the PDFs or their content on the site.** Short quotes only, each with its page.
- Everything else in `docs/` (the eight-part textbook, the old handbook, guides, notes) is optional background,
  not part of the plan.

## 3. Schedule

| Dates (Hobart) | Work |
|---|---|
| 10 Nov 2026 | No tasks |
| 11–21 Nov | **Foundations.** One connected walkthrough (§4). By 21 Nov Chris can explain, unaided: (a) how electricity gets from a generator through the network to a customer in Tasmania, and who is responsible at each point; (b) how AEMO balances supply and demand and coordinates dispatch, and how a network limit can affect the outcome; (c) how TasNetworks uses forecasts, asset ratings and other network constraints to plan capacity and screen new loads |
| 22 Nov–31 Dec | **The rest of both PDFs:** rules and participants, spot pricing, frequency and ancillary services, metering and settlement, financial markets (enough to explain their role), Tasmania's network development, asset planning, security and reliability. Some topics are a worked example, a diagram or a process walkthrough; not every one needs a simulator |

The coverage map (`website/content/coverage.json`) maps every module, lesson, chapter and section to a topic.
Use it to catch omissions; `tests/test_site.py` fails if anything is unmapped.

## 4. The foundations walkthrough

One connected walkthrough, built step by step with Chris:

1. **Follow the electricity through Tasmania:** generator to customer, and who is responsible at each point.
2. **Change demand in a simple dispatch simulation,** and see how a network limit changes the outcome.
3. **A hypothetical large load asks to connect.** Use the **Creek Road** screening example to show what a
   published capacity figure can and can't tell us (APR p. 63 Table 4-1; p. 69 Table 4-6; p. 71 Table 4-7).

Keep each interaction small enough for Chris to understand and help build.

## 5. How to teach: build with Chris

Every session follows the same loop:

**read a short section → predict what will happen → build or change one thing → check the result → explain it in
your own words.**

- **Chris attempts first.** Give Chris a specific part of the logic, calculation or explanation to do. Wait for the
  answer; don't reveal it in advance.
- **Review Chris's reasoning before polishing anything.** Investigate mistakes rather than overwriting them.
- **Increase complexity only when Chris can explain the current step.**
- **Session plans** live in `docs/sessions/`, one file per session.

## 6. Labels: keep these visibly separate

- **Published figure:** from a named source, with its page or table.
- **Assumption:** something we chose, stated as such.
- **Simulated output:** produced by our own simplified model, true only within its assumptions.

**Never present a simplified model as AEMO's or TasNetworks' actual software or process.** The claim labels
[ASSUMED], [SIMULATED], [MEASURED] and [VERIFIED] still apply. [VERIFIED] always states its scope.

## 7. Tracking and the portfolio

- **Progress** (`website/content/progress.json`) tracks **read**, **built** and **can explain** separately.
  - Only Chris's own actions count. **Claude reading or reviewing a document never counts as Chris learning it.**
  - *Read* is added when Chris says a section has been read.
  - *Built* is added when Chris's own work on an exercise has been reviewed.
  - *Can explain* is added when Chris's own-words explanation has been reviewed and holds up.
  - Every entry has a date and evidence.
- **The portfolio** (`website/content/portfolio.json`) grows only from finished work. Each item shows:
  - the question investigated;
  - the source used;
  - what Chris built or worked out;
  - what the result cannot tell us.
- **No placeholders,** and no dates for features not yet started.
- **Unfinished ideas** go in a private backlog, never in this public repository. `private/` is git-ignored for local notes.

## 8. The site

- **One simple page structure:** `website/index.html` with `website/site.css`; content in `website/content/*.json`.
- **Extend it by adding sections or steps as they're finished.** Never ship empty sections.
- **The payments pages, Rail and the old lab and desk are not in the site's navigation.** The payments pages still
  exist at their old addresses, because `watcher.yml` and `daily.yml` keep writing `website/data/`.
- **Light theme.** Colours from the approved logo: forest `#1B422E`, teal `#498182`, paper `#FEFDF7`.
  Master logo: `website/assets/brand/lupine-logo-original.webp`; don't recolour or redraw it.

## 9. Working agreements

- **Branches:** work on a branch, in small reviewable commits. Merge to `main`, which deploys the site, only when
  Chris says "merge". Show the replacement before changing the live site.
- **Tests:** new logic ships with tests. CI (`ci.yml`) lists test files explicitly.
- **Free by default.** No paid services or API keys without explaining why first.
- **The repository is public.** No private information: birth data, addresses, contact details, CVs, private
  conversations.
- **Safety, if hardware ever returns:** 5 V USB only; no mains work (in Australia, licensed electricians only);
  no loose lithium cells; nothing left powered and unattended.

## 10. Before the reset (archive)

- Everything up to 10 November 2026 is recoverable:
  - commit `e43c704` on `main`;
  - the branch `claude/setup-lupine-v0-P6vaO`.
- That includes:
  - the payments decision engine (April to October 2026);
  - Rail and Cloked;
  - the October lab, Grid Desk's Connections desk and the old portfolio;
  - the handbook and study notes.
- **Code still in the repository** is unchanged and tested (36 tests in `tests/test_aiva.py`, `test_rail.py`,
  `test_cloked.py`); details are in `docs/architecture.md`.
- **Payments-era figures** are [ASSUMED] (see `docs/provenance.md`) and are never evidence about electricity networks.
