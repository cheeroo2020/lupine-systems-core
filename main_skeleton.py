# main_skeleton.py

from typing import List

from src.aiva.merge_engine import MergeEngine as RouteEngine
from src.rail.executor import RailExecutor
from src.cloked.auditor import ClokedLogger


def main() -> None:
    # Instantiate all three layers
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


if __name__ == "__main__":
    main()
