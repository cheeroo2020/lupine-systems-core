#!/usr/bin/env python3
"""
Lupine Systems – Walking Skeleton
Aiva (Intelligence) → Rail (Execution) → Cloked (Evidence)
"""

from __future__ import annotations

from typing import List, Tuple, Dict, Any
from uuid import uuid4

from src.aiva.merge_engine import RouteEngine
from src.rail.executor import RailExecutor
from src.rail.state_machine import TransactionState
from src.cloked.auditor import AuditChain
from src.cloked.capsule import EvidenceCapsule


def run_transaction_scenario() -> Tuple[TransactionState, List[Dict[str, Any]]]:
    """
    Run a single 'happy path' transaction through:
      - Aiva route engine
      - Rail executor (with retries + chaos monkey)
      - Return final state + structured Rail event log
    """
    print("🚀 Starting Lupine Systems Walking Skeleton\n")

    # 1. Ask Aiva for a route
    route_engine = RouteEngine()
    route = route_engine.get_best_route(start="NodeA", end="NodeB")
    print("🧠 AIVA Selected Route:", route)

    # 2. Execute via Rail
    executor = RailExecutor()
    final_state, event_log = executor.execute_transaction(route)

    print("\n=== RAIL FINAL STATE ===")
    print("State:", final_state.name)

    return final_state, event_log


def main() -> None:
    # Synthetic transaction ID for this run
    transaction_id = str(uuid4())

    # Run the happy-path transaction
    final_state, event_log = run_transaction_scenario()

    # Pretty-print the Rail event log
    print("\n=== 🧾 FINAL TRANSACTION RECEIPT (Rail Event Log) ===")
    for ev in event_log:
        print(ev)

    # 3. Build Cloked audit chain from Rail events
    print("\n🔐 Building Cloked Audit Chain...")
    audit_chain = AuditChain()

    # Feed events into the chain in order
    for ev in event_log:
        audit_chain.log_event(ev)

    # First integrity check (should be True)
    print("\n=== CLOKED: Integrity Check (Before Tamper) ===")
    clean_ok = audit_chain.verify_integrity()
    print("Integrity OK?", clean_ok)

    # Capture the clean final hash for the Evidence Capsule
    clean_final_hash = audit_chain.get_final_hash()

    # 4. Generate Evidence Capsule (for regulator / export)
    print("\n📦 GENERATING EVIDENCE CAPSULE...")
    capsule = EvidenceCapsule.create(
        transaction_id=transaction_id,
        events=event_log,
        audit_hash=clean_final_hash,
        schema_version="1.0",
    )

    capsule_json = capsule.to_json()
    print(capsule_json)

    # Optionally save to disk (uncomment if you want files created each run)
    # filename = f"capsule_{capsule.capsule_id}.json"
    # capsule.save_to_disk(filename)
    # print(f"\n💾 Capsule saved to: {filename}")

    # 5. Tamper test to prove the chain detects corruption
    print("\n⚠️ Tampering with chain for verification test...")
    if len(audit_chain.chain) > 1:
        audit_chain.chain[1]["event"]["tampered"] = True

    print("\n=== CLOKED: Integrity Check (After Tamper) ===")
    tampered_ok = audit_chain.verify_integrity()
    print("Integrity OK?", tampered_ok)

    print("\n🏁 End of Transaction")


if __name__ == "__main__":
    main()
