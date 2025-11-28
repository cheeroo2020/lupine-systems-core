# main_skeleton.py

from typing import List

from src.aiva.merge_engine import MergeEngine as RouteEngine
from src.aiva.medical_graph import MedicalGraph
from src.aiva.volatility_graph import VolatilityGraph, CorridorVolatilityContext
from src.rail.executor import RailExecutor
from src.cloked.auditor import ClokedLogger


def run_transaction_skeleton() -> None:
    """Original walking skeleton: Aiva → Rail → Cloked."""
    route_engine: RouteEngine = RouteEngine()
    rail_executor: RailExecutor = RailExecutor()
    logger: ClokedLogger = ClokedLogger()

    # --- AIVA LAYER ---
    print("=== AIVA: Computing route ===")
    route: List[str] = route_engine.get_best_route("NodeA", "NodeB")
    print(f"AIVA selected route: {route}")

    # --- RAIL LAYER ---
    print("\n=== RAIL: Executing route ===")
    final_state: str = rail_executor.execute_transaction(route)
    print(f"RAIL final state: {final_state}")

    # --- CLOKED LAYER ---
    print("\n=== CLOKED: Logging outcome ===")
    message = f"Transaction completed with state={final_state}, route={route}"
    logger.log_event("SYSTEM", message)


def run_medical_scenarios() -> None:
    """Story 1.7 – Medical viability fast vs slow route."""
    logger = ClokedLogger()
    med_graph = MedicalGraph()

    print("\n=== MEDICAL VIABILITY SCENARIOS (Story 1.7) ===")

    # Scenario A — Fast route (2 hours) → Should succeed
    payload = "Heart"
    duration_fast = 2.0  # hours
    temp_ok = 4.0        # °C within safe band

    viability_fast = med_graph.calculate_viability(payload, duration_fast, temp_ok)
    print(
        f"Scenario A — Fast {payload} route: "
        f"duration={duration_fast}h, temp={temp_ok}°C, "
        f"viability={viability_fast:.3f}"
    )
    logger.log_event(
        "MEDICAL",
        f"Scenario A fast route viability={viability_fast:.3f} "
        f"for payload={payload}, duration={duration_fast}h, temp={temp_ok}°C",
    )

    # Scenario B — Slow route (6 hours) → Should fail (viability = 0)
    duration_slow = 6.0  # hours (> 4h limit for Heart)
    viability_slow = med_graph.calculate_viability(payload, duration_slow, temp_ok)
    print(
        f"Scenario B — Slow {payload} route: "
        f"duration={duration_slow}h, temp={temp_ok}°C, "
        f"viability={viability_slow:.3f}"
    )
    logger.log_event(
        "MEDICAL",
        f"Scenario B slow route viability={viability_slow:.3f} "
        f"for payload={payload}, duration={duration_slow}h, temp={temp_ok}°C",
    )

    if viability_fast > 0.0:
        print("→ Scenario A verdict: OK (payload viable).")
    else:
        print("→ Scenario A verdict: FAILED (unexpected for fast route).")

    if viability_slow == 0.0:
        print("→ Scenario B verdict: FAILED as expected (payload non-viable).")
    else:
        print("→ Scenario B verdict: WARNING (expected 0.0 viability).")


def run_volatility_scenario() -> None:
    """
    Story 1.4 – Volatility Graph:
    Scenario C (Market Crash on AUD-SGD corridor).

    - Route: Sydney → Singapore (conceptually AUD-SGD)
    - Medical: Safe (2 hours, in-range temp)
    - Volatility: Dangerous (index 8.5 > threshold)
    - Expected: Aiva rejects route due to high FX volatility risk.
    """
    logger = ClokedLogger()
    med_graph = MedicalGraph()
    vol_graph = VolatilityGraph()

    print("\n=== VOLATILITY SCENARIO (Story 1.4 – Market Crash) ===")

    # Medical side – same as a "fast, safe" journey
    payload = "Heart"
    duration_hours = 2.0
    temp_celsius = 4.0

    viability = med_graph.calculate_viability(payload, duration_hours, temp_celsius)
    print(
        f"Medical check – {payload}: duration={duration_hours}h, "
        f"temp={temp_celsius}°C → viability={viability:.3f}"
    )

    # Volatility side – corridor AUD-SGD in a crash-like scenario
    corridor_id = "AUD-SGD"
    crash_vol_index = 8.5  # 0–10 scale, > 5 is considered unsafe

    ctx = CorridorVolatilityContext(
        corridor_id=corridor_id,
        market_volatility_index=crash_vol_index,
    )
    vol_score = vol_graph.get_volatility_score(ctx)

    print(
        f"Volatility check – corridor={corridor_id}, "
        f"index={crash_vol_index} → volatility_score={vol_score:.3f}"
    )

    if viability > 0.0 and vol_score == 0.0:
        print(
            "→ Scenario C verdict: REJECTED by Aiva due to high FX volatility risk "
            "(medical conditions were acceptable)."
        )
        logger.log_event(
            "AIVA",
            f"Scenario C rejected: high FX volatility risk on {corridor_id} "
            f"(index={crash_vol_index}), despite medical viability={viability:.3f}.",
        )
    else:
        print(
            "→ Scenario C verdict: Unexpected combination "
            f"(viability={viability:.3f}, volatility_score={vol_score:.3f})."
        )
        logger.log_event(
            "AIVA",
            f"Scenario C anomaly: viability={viability:.3f}, "
            f"volatility_score={vol_score:.3f} on {corridor_id}.",
        )


def main() -> None:
    # 1) Original Aiva → Rail → Cloked skeleton
    run_transaction_skeleton()

    # 2) Medical thermal-decay scenarios (Story 1.7)
    run_medical_scenarios()

    # 3) Volatility-driven rejection scenario (Story 1.4)
    run_volatility_scenario()


if __name__ == "__main__":
    main()
