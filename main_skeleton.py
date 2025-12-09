from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple
from uuid import uuid4

from src.aiva.merge_engine import RouteEngine
from src.rail.executor import RailExecutor
from src.rail.state_machine import TransactionState
from src.cloked.auditor import AuditChain
from src.cloked.capsule import EvidenceCapsule


def run_transaction_scenario() -> Tuple[TransactionState, List[Dict[str, Any]], List[str], str]:
    """
    Run a single "happy path" transaction through:
      - AIVA (route selection)
      - RAIL (execution with retries and structured events)
      - CLOKED (hashing will be done later in main)
    Returns:
      final_state: TransactionState enum (or equivalent)
      event_log:   List of RailEvent dictionaries
      route:       List of hop node IDs
      transaction_id: String ID for this movement
    """
    print("🚀 Starting Lupine Systems Walking Skeleton\n")

    # Random transaction id for this movement
    transaction_id = str(uuid4())

    # 1. Ask AIVA for a route (currently static in RouteEngine)
    route_engine = RouteEngine()
    # IMPORTANT: current RouteEngine.get_best_route() takes NO arguments
    route = route_engine.get_best_route()
    print("🧠 AIVA Selected Route:", route)

    # 2. Execute via RAIL
    executor = RailExecutor()
    final_state, event_log = executor.execute_transaction(route)

    print("\n=== RAIL FINAL STATE ===")
    state_label = final_state.name if hasattr(final_state, "name") else str(final_state)
    print("State:", state_label)

    return final_state, event_log, route, transaction_id


def build_audit_chain(event_log: List[Dict[str, Any]]) -> AuditChain:
    """
    Feed Rail events into Cloked's AuditChain and return the chain.
    """
    print("\n🔐 Building Cloked Audit Chain...")
    audit_chain = AuditChain()

    for ev in event_log:
        audit_chain.log_event(ev)

    print("\n=== CLOKED: Integrity Check (Before Tamper) ===")
    ok = audit_chain.verify_integrity()
    print("Integrity OK?", ok)

    # Deliberate tamper test (Story 5.1)
    print("\n⚠️ Tampering with chain for verification test...")
    if len(audit_chain.chain) > 1:
        # Add or change a field in the second entry to break the hash chain
        audit_chain.chain[1]["event"]["amount"] = 99999999

    print("\n=== CLOKED: Integrity Check (After Tamper) ===")
    ok_after = audit_chain.verify_integrity()
    print("Integrity OK?", ok_after)

    return audit_chain


def get_final_audit_hash(audit_chain: AuditChain) -> str:
    """
    Safely obtain the final hash from the audit chain.
    Supports both:
      - audit_chain.get_final_hash()
      - or directly reading the last entry's 'hash'
    """
    if hasattr(audit_chain, "get_final_hash"):
        return audit_chain.get_final_hash()  # type: ignore[attr-defined]

    if getattr(audit_chain, "chain", None):
        return audit_chain.chain[-1].get("hash", "")

    return ""


def generate_evidence_capsule(
    transaction_id: str,
    route: List[str],
    event_log: List[Dict[str, Any]],
    audit_chain: AuditChain,
) -> EvidenceCapsule:
    """
    Build an EvidenceCapsule from the transaction history and audit hash.
    """
    final_hash = get_final_audit_hash(audit_chain)

    # You can choose any schema_version here; default is "1.0" in capsule class.
    capsule = EvidenceCapsule(
        transaction_id=transaction_id,
        events=event_log,
        audit_hash=final_hash,
    )

    print("\n📦 GENERATING EVIDENCE CAPSULE...\n")
    capsule_json = capsule.to_json()
    print(capsule_json)

    # Optionally persist to disk (uncomment if you want a file)
    # capsule.save_to_disk(f"capsule_{transaction_id}.json")

    return capsule


def print_transaction_receipt(event_log: List[Dict[str, Any]]) -> None:
    """
    Pretty-print the Rail event log as a transaction receipt.
    """
    print("\n=== 🧾 FINAL TRANSACTION RECEIPT (Rail Event Log) ===")
    for ev in event_log:
        print(json.dumps(ev, indent=2))


def main() -> None:
    # 1. Run the transaction through AIVA + RAIL
    final_state, event_log, route, transaction_id = run_transaction_scenario()

    # 2. Show structured Rail event log
    print_transaction_receipt(event_log)

    # 3. Build and test CLOKED AuditChain integrity
    audit_chain = build_audit_chain(event_log)

    # 4. Generate Cloked Evidence Capsule
    generate_evidence_capsule(
        transaction_id=transaction_id,
        route=route,
        event_log=event_log,
        audit_chain=audit_chain,
    )

    print("\n🏁 End of Transaction\n")


if __name__ == "__main__":
    main()
