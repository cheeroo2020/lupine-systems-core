# Lupine Systems V0 — Specification

## One-line definition

Lupine decides how value moves when the cost of getting it wrong is high.

## V0 scope

- Take a movement request
- Compare route options (Aiva-lite)
- Choose the best route with explanation
- Simulate execution (Rail-lite)
- Produce a full evidence log (Cloked-lite)

## Out of scope for V0

- Real bank integrations
- Live FX APIs
- Real compliance screening
- Blockchain anchoring
- Medical payload logic

## Success criteria

1. User can enter a movement request
2. System auto-selects a route
3. Decision is clearly explained
4. Execution is simulated end to end
5. A full evidence log is generated

## Demo scenario

- Amount: AUD 500,000
- To: SGD
- Urgency: high
- Expected: Fast Route or Balanced Route selected with rationale
