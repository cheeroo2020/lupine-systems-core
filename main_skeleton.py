import uuid
from datetime import datetime
import json

from src.aiva.merge_engine import RouteEngine
from src.rail.executor import RailExecutor
from src.rail.state_machine import TransactionState
from src.cloked.auditor import AuditChain
from src.cloked.capsule import EvidenceCapsule


def print_event_log(event_log):
    print("\n=== 🧾 FINAL TRANSACTION RECEIPT (Rail Event Log) ===")
    for ev in event_log:
        print(json.dumps(ev, indent=2))


def generate_evidence_capsule(transaction_id, event_log, audit_chain):
    print("\n📦 GENERATING EVIDENCE CAPSULE...\n")

    capsule = EvidenceCapsule(
        capsule_id=str(uuid.uuid4()),
        transaction_id=transaction_id,
        generated_at=datetime.utcnow().isoformat() + "Z",
        schema_version="1.0",
        events=event_log,
        audit_hash=audit_chain.get_final_hash()
    )

    capsule_json = capsule.to_json()
    print(capsule_json)

    capsule.save_to_disk(f"evidence_capsule_{transaction_id}.json")

    return capsule


def run_transaction_scenario():
    route_engine = RouteEngine()

    # get_best_route is now origin=, destination=
    route = route_engine.get_best_route(origin="NodeA", destination="NodeB")

    print("\n🧠 AIVA Selected Route:", route)

    rail_exec = RailExecutor()
    final_state, event_log = rail_exec.execute_transaction(route)

    return final_state, event_log, str(uuid.uuid4())


def main():
    print("\n🚀 Starting Lupine Systems Walking Skeleton\n")

    final_state, event_log, transaction_id = run_transaction_scenario()

    print("\n=== RAIL FINAL STATE ===")
    print("State:", final_state.name)

    print_event_log(event_log)

    print("\n🔐 Building Cloked Audit Chain...\n")
    audit_chain = AuditChain()

    for ev in event_log:
        audit_chain.log_event(ev)

    print("=== CLOKED: Integrity Check (Before Tamper) ===")
    print("Integrity OK?", audit_chain.verify_integrity())

    # Tamper test
    print("\n⚠️ Tampering with chain for verification test...\n")
    audit_chain.chain[1]["event"]["event_type"] = "TAMPERED_DATA"

    print("=== CLOKED: Integrity Check (After Tamper) ===")
    print("Integrity OK?", audit_chain.verify_integrity())

    # Create final evidence capsule
    generate_evidence_capsule(
        transaction_id=transaction_id,
        event_log=event_log,
        audit_chain=audit_chain
    )

    print("\n🏁 End of Transaction\n")


if __name__ == "__main__":
    main()
