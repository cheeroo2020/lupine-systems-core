# tests/test_risk_scenarios.py

"""
Lupine Systems — Risk Scenario Test Suite

Scenarios:
  A – Medical viability (fast vs slow route)
  B – Volatility risk (market crash)
  C – Compliance risk (sanctions / blacklist)
  D – Liquidity crunch (insufficient funds)
  E – Combined liquidity scenario (already covered by D)
  F – Rail resilience (retry / failover behaviour)
"""

from __future__ import annotations

from typing import List

from src.aiva.medical_graph import MedicalGraph
from src.aiva.volatility_graph import VolatilityGraph
from src.aiva.compliance_graph import ComplianceGraph
from src.aiva.liquidity_graph import LiquidityGraph
from src.aiva.merge_engine import MergeEngine as RouteEngine
from src.rail.executor import RailExecutor
from src.cloked.auditor import ClokedLogger


# ---------- Helpers ----------


def _print_divider() -> None:
    print("\n" + "#" * 10 + " LUPINE RISK SCENARIOS — TEST SUITE " + "#" * 10 + "\n")


# ---------- Scenario A: Medical Viability (Story 1.7) ----------


def test_scenario_a_medical(logger: ClokedLogger) -> None:
    print("=== SCENARIO A — MEDICAL VIABILITY (Story 1.7) ===")
    medical = MedicalGraph()

    payload = "Heart"
    duration_fast = 2.0
    duration_slow = 6.0
    temp_ok = 4.0

    # Fast route
    viability_fast = medical.calculate_viability(
        payload_type=payload,
        duration_hours=duration_fast,
        temp_celsius=temp_ok,
    )
    print(
        f"Scenario A — Fast Heart route: duration={duration_fast}h, "
        f"temp={temp_ok}°C, viability={viability_fast:.3f}"
    )
    logger.log_event(
        "MEDICAL",
        (
            f"Scenario A fast route viability={viability_fast:.3f} for "
            f"payload={payload}, duration={duration_fast}h, temp={temp_ok}°C"
        ),
    )

    # Slow route
    viability_slow = medical.calculate_viability(
        payload_type=payload,
        duration_hours=duration_slow,
        temp_celsius=temp_ok,
    )
    print(
        f"Scenario B — SLOW Heart route: duration={duration_slow}h, "
        f"temp={temp_ok}°C, viability={viability_slow:.3f}"
    )
    logger.log_event(
        "MEDICAL",
        (
            f"Scenario B slow route viability={viability_slow:.3f} for "
            f"payload={payload}, duration={duration_slow}h, temp={temp_ok}°C"
        ),
    )

    print(
        "-> Scenario A verdict: OK (payload viable)."
        if viability_fast > 0.0
        else "-> Scenario A verdict: FAILED (payload non-viable)."
    )
    print(
        "-> Scenario B verdict: FAILED as expected (payload non-viable)."
        if viability_slow == 0.0
        else "-> Scenario B verdict: WARNING – expected non-viable."
    )


# ---------- Scenario C: Volatility Risk (Story 1.4) ----------


def test_scenario_c_volatility(logger: ClokedLogger) -> None:
    print("\n=== SCENARIO C — VOLATILITY SCENARIO (Story 1.4 — Market Crash) ===")

    medical = MedicalGraph()
    vol = VolatilityGraph()

    payload = "Heart"
    duration = 2.0
    temp_ok = 4.0
    corridor = "AUD-SGD"
    crash_index = 8.5

    viability = medical.calculate_viability(
        payload_type=payload,
        duration_hours=duration,
        temp_celsius=temp_ok,
    )
    volatility_score = vol.calculate_score(
        corridor_id=corridor,
        market_volatility_index=crash_index,
    )

    print(
        f"Medical check — Heart: duration={duration}h, temp={temp_ok}°C "
        f"-> viability={viability:.3f}"
    )
    print(
        f"Volatility check — corridor={corridor}, index={crash_index} "
        f"-> volatility_score={volatility_score:.3f}"
    )

    if volatility_score == 0.0:
        print(
            "-> Scenario C verdict: REJECTED by Aiva due to high FX volatility "
            "risk (medical conditions were acceptable)."
        )
    else:
        print("-> Scenario C verdict: WARNING – volatility score not zero.")

    logger.log_event(
        "AIVA",
        (
            "Scenario C rejected: high FX volatility risk on "
            f"{corridor} (index={crash_index}), despite medical "
            f"viability={viability:.3f}."
        ),
    )


# ---------- Scenario D: Compliance Risk (Story 1.5) ----------


def test_scenario_d_compliance(logger: ClokedLogger) -> None:
    print("\n=== SCENARIO D — COMPLIANCE SCENARIO (Story 1.5 – Sanctions Violation) ===")

    medical = MedicalGraph()
    vol = VolatilityGraph()
    comp = ComplianceGraph()

    payload = "Heart"
    duration = 2.0
    temp_ok = 4.0
    corridor = "AUD-KPW"  # AUD to North Korean Won
    vol_index = 1.0
    destination = "North Korea"
    beneficiary = "BEN-SDNTK-001"

    viability = medical.calculate_viability(
        payload_type=payload,
        duration_hours=duration,
        temp_celsius=temp_ok,
    )
    volatility_score = vol.calculate_score(
        corridor_id=corridor,
        market_volatility_index=vol_index,
    )
    compliance_score = comp.calculate_score(
        destination_country=destination,
        beneficiary_id=beneficiary,
    )

    print(
        f"Medical check — Heart: duration={duration}h, temp={temp_ok}°C "
        f"-> viability={viability:.3f}"
    )
    print(
        f"Volatility check — corridor={corridor}, index={vol_index} "
        f"-> volatility_score={volatility_score:.3f}"
    )
    print(
        "Compliance check — destination="
        f"{destination}, beneficiary={beneficiary} "
        f"-> compliance_score={compliance_score:.3f}"
    )

    if compliance_score == 0.0:
        print(
            "-> Scenario D verdict: REJECTED by Aiva due to Compliance Failure "
            "(Sanctions / Blacklisted Destination)."
        )
    else:
        print("-> Scenario D verdict: WARNING – expected hard compliance reject.")

    logger.log_event(
        "AIVA",
        (
            "Scenario D rejected: sanctions/compliance failure for "
            f"destination={destination}, beneficiary={beneficiary}. "
            f"Medical viability={viability:.3f}, volatility_score={volatility_score:.3f}."
        ),
    )


# ---------- Scenario E: Liquidity Crunch (Story 1.3) ----------


def test_scenario_e_liquidity(logger: ClokedLogger) -> None:
    print("\n=== SCENARIO E — LIQUIDITY SCENARIO (Story 1.3 — Liquidity Crunch) ===")

    medical = MedicalGraph()
    vol = VolatilityGraph()
    comp = ComplianceGraph()
    liq = LiquidityGraph()

    payload = "Heart"
    duration = 2.0
    temp_ok = 4.0
    corridor = "AUD-SGD"
    vol_index = 1.0
    destination = "Singapore"
    beneficiary = "BEN-SG-001"
    node = "Bank_Singapore"
    amount = 75_000.00

    viability = medical.calculate_viability(
        payload_type=payload,
        duration_hours=duration,
        temp_celsius=temp_ok,
    )
    volatility_score = vol.calculate_score(
        corridor_id=corridor,
        market_volatility_index=vol_index,
    )
    compliance_score = comp.calculate_score(
        destination_country=destination,
        beneficiary_id=beneficiary,
    )
    liquidity_score = liq.calculate_score(
        node_id=node,
        transaction_amount=amount,
    )

    print(
        f"Medical check — Heart: duration={duration}h, temp={temp_ok}°C "
        f"-> viability={viability:.3f}"
    )
    print(
        f"Volatility check — corridor={corridor}, index={vol_index} "
        f"-> volatility_score={volatility_score:.3f}"
    )
    print(
        f"Compliance check — destination={destination}, "
        f"beneficiary={beneficiary} -> compliance_score={compliance_score:.3f}"
    )
    print(
        f"Liquidity check — node={node}, amount={amount:.2f} "
        f"-> liquidity_score={liquidity_score:.3f}"
    )

    if liquidity_score == 0.0:
        print(
            "-> Scenario E verdict: REJECTED by Aiva due to Insufficient "
            "Liquidity at intermediate settlement node."
        )
    else:
        print("-> Scenario E verdict: WARNING – expected insufficient liquidity.")

    logger.log_event(
        "AIVA",
        (
            "Scenario E rejected: insufficient liquidity at node "
            f"{node} for amount={amount:.2f}. Medical viability={viability:.3f}, "
            f"volatility_score={volatility_score:.3f}, compliance_score={compliance_score:.3f}."
        ),
    )


# ---------- Scenario F: Rail Resilience (Story 4.3) ----------


def test_scenario_f_resilience(logger: ClokedLogger) -> None:
    print("\n=== SCENARIO F — RAIL RESILIENCE SCENARIO (Story 4.3) ===")

    route_engine: RouteEngine = RouteEngine()
    rail_executor: RailExecutor = RailExecutor()

    # Ask Aiva for a simple route
    route: List[str] = route_engine.get_best_route("NodeA", "NodeB")
    print(f"AIVA (for Scenario F) selected route: {route}")

    print(">>> RAIL: Liquidity locked for route:", route)
    print(">>> RAIL: Executing route with retry + chaos monkey enabled...")

    final_status, events = rail_executor.execute_transaction(route)

    print(f"Final Rail state for Scenario F: {final_status}")
    logger.log_event(
        "RAIL",
        (
            f"Scenario F completed with final_state={final_status}, "
            f"route={route}"
        ),
    )

    # Note: events are already printed by RailExecutor as JSON lines.
    # If needed we could also inspect them here.


# ---------- Test Runner ----------


def run_all_tests() -> None:
    logger = ClokedLogger()
    _print_divider()

    test_scenario_a_medical(logger)
    test_scenario_c_volatility(logger)
    test_scenario_d_compliance(logger)
    test_scenario_e_liquidity(logger)
    test_scenario_f_resilience(logger)

    print("\n########## END OF TEST SUITE ##########\n")


if __name__ == "__main__":
    run_all_tests()
