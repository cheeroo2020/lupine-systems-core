<p align="center">
  <img src="website/assets/brand/lupine-logo.png" alt="Lupine" width="200">
</p>

# Lupine

**An interactive learning website that grows into a live technical portfolio.** It follows how AEMO runs the
National Electricity Market, how TasNetworks plans and operates Tasmania's transmission and distribution
networks, and where their responsibilities meet. It is built by Chris Gogoi in Hobart, one finished piece at a time.

**Site:** [cheeroo2020.github.io/lupine-systems-core](https://cheeroo2020.github.io/lupine-systems-core/)

## How it's built

- **Two sources:** AEMO's *NEM Foundations* eLearning (2026) and TasNetworks' *Annual Planning Report 2026*.
  The site cites them by module, lesson and page; it never reproduces them.
- **A coverage map** (`website/content/coverage.json`) assigns every module and chapter to a topic, says what
  will be built to learn it, and shows what has been read, built and explained.
- **The portfolio** shows only finished work. Each item gives the question, the source, what was built or
  worked out, and what the result can't tell us.
- **Labels keep three things apart:** published figures, assumptions, and simulated outputs. A simplified
  model is never presented as AEMO's or TasNetworks' own software or process.

Working rules for contributors, including AI agents, are in [CLAUDE.md](CLAUDE.md).

## Run the checks

```bash
pip install -r requirements.txt
PYTHONPATH=. pytest tests/test_site.py tests/test_aiva.py tests/test_rail.py tests/test_cloked.py
```

To preview the site locally: `cd website && python3 -m http.server`, then open http://localhost:8000.

## Before November 2026

Lupine began as a payments decision engine, and in October 2026 became an energy-learning project with a lab
and a "Grid Desk". All of it is recoverable from commit `e43c704` on `main` and from the branch
`claude/setup-lupine-v0-P6vaO`. The remaining code (`src/`) and its tests are described in
[docs/architecture.md](docs/architecture.md).

## License

See [LICENSE](LICENSE). © Chirantan Gogoi.
