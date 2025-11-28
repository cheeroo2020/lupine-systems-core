# src/aiva/volatility_graph.py

from __future__ import annotations

from dataclasses import dataclass


MAX_VOLATILITY_THRESHOLD: float = 5.0  # 0–10 scale, 5+ is considered unsafe


@dataclass(frozen=True)
class CorridorVolatilityContext:
    """
    Simple context object for a corridor.

    For now, we only care about:
    - corridor_id: e.g. "AUD-SGD", "AUD-USD"
    - market_volatility_index: 0.0 (calm) → 10.0 (crash)
    """
    corridor_id: str
    market_volatility_index: float


class VolatilityGraph:
    """
    Models corridor safety based on a simple volatility index.

    Rules:
    - market_volatility_index > MAX_VOLATILITY_THRESHOLD → score = 0.0 (unsafe)
    - otherwise: score is normalized between 0.1 and 1.0
      with lower volatility → higher score.

    This is a deliberately simple version of the volatility model from
    the Lupine book, suitable for early Aiva risk gating and pre-checks.
    """

    def get_volatility_score(self, ctx: CorridorVolatilityContext) -> float:
        """
        Compute a normalized volatility score for a corridor.

        Parameters
        ----------
        ctx : CorridorVolatilityContext
            Corridor identifier + volatility index (0.0 – 10.0).

        Returns
        -------
        float
            Volatility score in [0.0, 1.0].
            - 0.0 means "reject corridor" (too volatile)
            - (0.1, 1.0] means "usable", higher = safer
        """
        v = ctx.market_volatility_index

        # Hard reject if above threshold
        if v > MAX_VOLATILITY_THRESHOLD:
            return 0.0

        # Clamp within expected bounds just to be safe
        if v < 0.0:
            v = 0.0
        if v > MAX_VOLATILITY_THRESHOLD:
            v = MAX_VOLATILITY_THRESHOLD

        # Map [0, threshold] → [1.0, 0.1]
        # 0.0 volatility → 1.0 (perfectly calm)
        # threshold      → 0.1 (barely acceptable)
        if MAX_VOLATILITY_THRESHOLD == 0:
            return 1.0  # avoid division by zero, degenerate case

        remaining_fraction = (MAX_VOLATILITY_THRESHOLD - v) / MAX_VOLATILITY_THRESHOLD
        score = 0.1 + remaining_fraction * 0.9

        # Clamp + round for cleaner output
        return max(0.0, min(1.0, round(score, 3)))


if __name__ == "__main__":
    graph = VolatilityGraph()
    calm_ctx = CorridorVolatilityContext(corridor_id="AUD-SGD", market_volatility_index=1.2)
    crash_ctx = CorridorVolatilityContext(corridor_id="AUD-SGD", market_volatility_index=8.5)

    print("Calm corridor score:", graph.get_volatility_score(calm_ctx))
    print("Crash corridor score:", graph.get_volatility_score(crash_ctx))

