# main_skeleton.py

from typing import List
import json

from src.aiva.merge_engine import MergeEngine as RouteEngine
from src.rail.executor import RailExecutor
from src.cloked.auditor import ClokedLogger
from src.rail.state_machine import TransactionState


def run_happy_path_demo() -> None:
    """
    Happy Path Demo:
    - Aiva computes a route
    - Rail executes it (with structured events)
    - Cloked logs final outcome
    - We print a Transaction Receipt (full Rail event log)
    """
    route_engine: RouteEngine = RouteEngine()
    rail_executor: RailExecutor = RailExecutor()
    logger: ClokedLogger = ClokedLogger()

    print("=== LUPINE SYSTEMS – HAPPY PATH DEMO ===")

    # --- AIVA LAYER ---
    print("=== AIVA: Computing route ===")
    route: List[str] = route_engine.get_best_route("NodeA", "NodeB")
    print(f"AIVA selected route: {route}")

    # --- RAIL LAYER ---
    print("\n=== RAIL: Executing route (structured events) ===")
    final_state: TransactionState = rail_executor.execute_transaction(route)

    # --- CLOKED LAYER ---
    print("\n=== CLOKED: Logging outcome ===")
    message = (
        f"Transaction completed with state={final_state.name}, "
        f"code={final_state.value}, route={route}"
    )
    logger.log_event("SYSTEM", message)

    # --- TRANSACTION RECEIPT ---
    print("\n=== TRANSACTION RECEIPT (Rail Event Log) ===")
    for event in rail_executor.event_log:
        print(json.dumps(event.to_dict(), indent=2, ensure_ascii=False))


def main() -> None:
    # For now, just run the happy path.
    # All risk scenarios live in tests/test_risk_scenarios.py
    run_happy_path_demo()


if __name__ == "__main__":
    main()
