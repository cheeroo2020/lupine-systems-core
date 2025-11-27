# main_skeleton.py

from typing import List

from src.aiva.merge_engine import MergeEngine as RouteEngine
from src.aiva.medical_graph import MedicalGraph
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
    """New logic test: Medical viability for fast vs slow routes."""
    logger = ClokedLogger()
    med_graph = MedicalGraph()

    print("\n=== MEDICAL VIABILITY SCENARIOS (Story 1.7) ===")

    # Scenario A — Fast route (2 hours) → Should succeed (viability > 0)
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

    # Simple semantic verdicts
    if viability_fast > 0.0:
        print("→ Scenario A verdict: OK (payload viable).")
    else:
        print("→ Scenario A verdict: FAILED (unexpected for fast route).")

    if viability_slow == 0.0:
        print("→ Scenario B verdict: FAILED as expected (payload non-viable).")
    else:
        print("→ Scenario B verdict: WARNING (expected 0.0 viability).")


def main() -> None:
    # 1) Run the original Aiva → Rail → Cloked skeleton
    run_transaction_skeleton()

    # 2) Run new Story 1.7 medical urgency logic
    run_medical_scenarios()


if __name__ == "__main__":
    main()
