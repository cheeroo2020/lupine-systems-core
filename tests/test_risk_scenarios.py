# tests/test_risk_scenarios.py

from src.aiva.medical_graph import MedicalGraph
from src.aiva.volatility_graph import VolatilityGraph, CorridorVolatilityContext
from src.aiva.compliance_graph import ComplianceGraph, ComplianceContext
from src.aiva.liquidity_graph import LiquidityGraph, LiquidityContext
from src.aiva.merge_engine import MergeEngine as RouteEngine
from src.rail.executor import RailExecutor
from src.rail.state_machine import TransactionState
from src.cloked.auditor import ClokedLogger


def run_medical_scenarios() -> None:
    logger = ClokedLogger()
    med_graph = MedicalGraph()

    print("\n=== MEDICAL VIABILITY SCENARIOS (Story 1.7) ===")

    payload = "Heart"
    temp_ok = 4.0

    # Scenario A – Fast route
    duration_fast = 2.0
    viability_fast = med_graph.calculate_viability(payload, duration_fast, temp_ok)
    print(
        f"Scenario A — Fast {payload} route: "
        f"duration={duration_fast}h, temp={temp_ok}C, "
        f"viability={viability_fast:.3f}"
    )
    logger.log_event(
        "MEDICAL",
        (
            f"Scenario A fast route viability={viability_fast:.3f} "
            f"for payload={payload}, duration={duration_fast}h, temp={temp_ok}C"
        ),
    )

    # Scenario B – Slow route (should fail)
    duration_slow = 6.0
    viability_slow = med_graph.calculate_viability(payload, duration_slow, temp_ok)
    print(
        f"Scenario B — Slow {payload} route: "
        f"duration={duration_slow}h, temp={temp_ok}C, "
        f"viability={viability_slow:.3f}"
    )
    logger.log_event(
        "MEDICAL",
        (
            f"Scenario B slow route viability={viability_slow:.3f} "
            f"for payload={payload}, duration={duration_slow}h, temp={temp_ok}C"
        ),
    )

    if viability_fast > 0.0:
        print("-> Scenario A verdict: OK (payload viable).")
    else:
        print("-> Scenario A verdict: FAILED (unexpected for fast route).")

    if viability_slow == 0.0:
        print("-> Scenario B verdict: FAILED as expected (payload non-viable).")
    else:
        print("-> Scenario B verdict: WARNING (expected 0.0 viability).")


def run_volatility_scenario() -> None:
    logger = ClokedLogger()
    med_graph = MedicalGraph()
    vol_graph = VolatilityGraph()

    print("\n=== VOLATILITY SCENARIO (Story 1.4 – Market Crash) ===")

    payload = "Heart"
    duration_hours = 2.0
    temp_celsius = 4.0

    viability = med_graph.calculate_viability(payload, duration_hours, temp_celsius)
    print(
        f"Medical check – {payload}: duration={duration_hours}h, "
        f"temp={temp_celsius}C -> viability={viability:.3f}"
    )

    corridor_id = "AUD-SGD"
    crash_vol_index = 8.5

    ctx = CorridorVolatilityContext(
        corridor_id=corridor_id,
        market_volatility_index=crash_vol_index,
    )
    vol_score = vol_graph.get_volatility_score(ctx)

    print(
        f"Volatility check – corridor={corridor_id}, "
        f"index={crash_vol_index} -> volatility_score={vol_score:.3f}"
    )

    if viability > 0.0 and vol_score == 0.0:
        print(
            "-> Scenario C verdict: REJECTED by Aiva due to high FX volatility risk "
            "(medical conditions were acceptable)."
        )
        logger.log_event(
            "AIVA",
            (
                f"Scenario C rejected: high FX volatility risk on {corridor_id} "
                f"(index={crash_vol_index}), despite medical viability={viability:.3f}."
            ),
        )
    else:
        print(
            "-> Scenario C verdict: Unexpected combination "
            f"(viability={viability:.3f}, volatility_score={vol_score:.3f})."
        )
        logger.log_event(
            "AIVA",
            (
                "Scenario C anomaly: "
                f"viability={viability:.3f}, volatility_score={vol_score:.3f} "
                f"on {corridor_id}."
            ),
        )


def run_compliance_scenario() -> None:
    logger = ClokedLogger()
    med_graph = MedicalGraph()
    vol_graph = VolatilityGraph()
    comp_graph = ComplianceGraph()

    print("\n=== COMPLIANCE SCENARIO (Story 1.5 – Sanctions Violation) ===")

    payload = "Heart"
    duration_hours = 2.0
    temp_celsius = 4.0

    viability = med_graph.calculate_viability(payload, duration_hours, temp_celsius)
    print(
        f"Medical check – {payload}: duration={duration_hours}h, "
        f"temp={temp_celsius}C -> viability={viability:.3f}"
    )

    corridor_id = "AUD-KPW"
    calm_vol_index = 1.0

    vol_ctx = CorridorVolatilityContext(
        corridor_id=corridor_id,
        market_volatility_index=calm_vol_index,
    )
    vol_score = vol_graph.get_volatility_score(vol_ctx)
    print(
        f"Volatility check – corridor={corridor_id}, "
        f"index={calm_vol_index} -> volatility_score={vol_score:.3f}"
    )

    destination_country = "North Korea"
    beneficiary_id = "BEN-SDNTK-001"

    comp_ctx = ComplianceContext(
        destination_country=destination_country,
        beneficiary_id=beneficiary_id,
    )
    comp_score = comp_graph.get_compliance_score(comp_ctx)
    print(
        f"Compliance check – destination={destination_country}, "
        f"beneficiary={beneficiary_id} -> compliance_score={comp_score:.3f}"
    )

    if viability > 0.0 and vol_score > 0.0 and comp_score == 0.0:
        print(
            "-> Scenario D verdict: REJECTED by Aiva due to "
            "Compliance Failure (Sanctions / Blacklisted Destination)."
        )
        logger.log_event(
            "AIVA",
            (
                "Scenario D rejected: sanctions/compliance failure for "
                f"destination={destination_country}, beneficiary={beneficiary_id}. "
                f"Medical viability={viability:.3f}, "
                f"volatility_score={vol_score:.3f}."
            ),
        )
    else:
        print(
            "-> Scenario D verdict: Unexpected combination "
            f"(viability={viability:.3f}, volatility_score={vol_score:.3f}, "
            f"compliance_score={comp_score:.3f})."
        )
        logger.log_event(
            "AIVA",
            (
                "Scenario D anomaly: "
                f"viability={viability:.3f}, volatility_score={vol_score:.3f}, "
                f"compliance_score={comp_score:.3f} for "
                f"destination={destination_country}, beneficiary={beneficiary_id}."
            ),
        )


def run_liquidity_scenario() -> None:
    logger = ClokedLogger()
    med_graph = MedicalGraph()
    vol_graph = VolatilityGraph()
    comp_graph = ComplianceGraph()
    liq_graph = LiquidityGraph()

    print("\n=== LIQUIDITY SCENARIO (Story 1.3 – Liquidity Crunch) ===")

    payload = "Heart"
    duration_hours = 2.0
    temp_celsius = 4.0

    viability = med_graph.calculate_viability(payload, duration_hours, temp_celsius)
    print(
        f"Medical check – {payload}: duration={duration_hours}h, "
        f"temp={temp_celsius}C -> viability={viability:.3f}"
    )

    corridor_id = "AUD-SGD"
    calm_vol_index = 1.0

    vol_ctx = CorridorVolatilityContext(
        corridor_id=corridor_id,
        market_volatility_index=calm_vol_index,
    )
    vol_score = vol_graph.get_volatility_score(vol_ctx)
    print(
        f"Volatility check – corridor={corridor_id}, "
        f"index={calm_vol_index} -> volatility_score={vol_score:.3f}"
    )

    destination_country = "Singapore"
    beneficiary_id = "BEN-SG-001"

    comp_ctx = ComplianceContext(
        destination_country=destination_country,
        beneficiary_id=beneficiary_id,
    )
    comp_score = comp_graph.get_compliance_score(comp_ctx)
    print(
        f"Compliance check – destination={destination_country}, "
        f"beneficiary={beneficiary_id} -> compliance_score={comp_score:.3f}"
    )

    node_id = "Bank_Singapore"
    transaction_amount = 75_000.0

    liq_ctx = LiquidityContext(
        node_id=node_id,
        transaction_amount=transaction_amount,
    )
    liq_score = liq_graph.get_liquidity_score(liq_ctx)
    print(
        f"Liquidity check – node={node_id}, "
        f"amount={transaction_amount:.2f} -> liquidity_score={liq_score:.3f}"
    )

    if (
        viability > 0.0
        and vol_score > 0.0
        and comp_score > 0.0
        and liq_score == 0.0
    ):
        print(
            "-> Scenario E verdict: REJECTED by Aiva due to "
            "Insufficient Liquidity at intermediate settlement node."
        )
        logger.log_event(
            "AIVA",
            (
                "Scenario E rejected: insufficient liquidity at node "
                f"{node_id} for amount={transaction_amount:.2f}. "
                f"Medical viability={viability:.3f}, "
                f"volatility_score={vol_score:.3f}, "
                f"compliance_score={comp_score:.3f}."
            ),
        )
    else:
        print(
            "-> Scenario E verdict: Unexpected combination "
            f"(viability={viability:.3f}, volatility_score={vol_score:.3f}, "
            f"compliance_score={comp_score:.3f}, liquidity_score={liq_score:.3f})."
        )
        logger.log_event(
            "AIVA",
            (
                "Scenario E anomaly: "
                f"viability={viability:.3f}, volatility_score={vol_score:.3f}, "
                f"compliance_score={comp_score:.3f}, liquidity_score={liq_score:.3f} "
                f"for node={node_id}, amount={transaction_amount:.2f}."
            ),
        )


def test_scenario_f_resilience() -> None:
    """
    Scenario F – Rail Resilience under Network Glitches.

    Goal:
    - Run a standard transaction using RailExecutor.
    - Because of the 25% failure chance per hop, we might see:
        - Full success with no retries,
        - Success after some retries,
        - Or full failure after MAX_RETRIES.
    - The important part is observing the retry logs and final state.
    """
    logger = ClokedLogger()
    route_engine = RouteEngine()
    rail_executor = RailExecutor()

    print("\n=== SCENARIO F – RAIL RESILIENCE (Story 4.3) ===")

    route = route_engine.get_best_route("NodeA", "NodeB")
    print(f"AIVA (for Scenario F) selected route: {route}")

    final_state: TransactionState = rail_executor.execute_transaction(route)
    print(f"Final Rail state for Scenario F: {final_state.name} ({final_state.value})")

    logger.log_event(
        "RAIL",
        (
            "Scenario F completed with final_state="
            f"{final_state.name} ({final_state.value}), route={route}"
        ),
    )


def run_all_tests() -> None:
    print("\n########## LUPINE RISK SCENARIOS – TEST SUITE ##########")
    run_medical_scenarios()
    run_volatility_scenario()
    run_compliance_scenario()
    run_liquidity_scenario()
    test_scenario_f_resilience()
    print("\n########## END OF TEST SUITE ##########")


if __name__ == "__main__":
    run_all_tests()
