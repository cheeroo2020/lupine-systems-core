import uuid
import json
from datetime import datetime

from src.aiva.merge_engine import RouteEngine
from src.rail.executor import RailExecutor
from src.cloked.auditor import AuditChain
from src.cloked.capsule import EvidenceCapsule


def normalise_event(ev):
    """
    Ensure we always work with plain dicts.

    If this is a RailEvent object, use its to_dict().
    If it is already a dict, just return it.
    """
    if hasattr(ev, "to_dict"):
        return ev.to_dict()
    return ev


def print_event_log(event_log):
    """Pretty-print the structured Rail events."""
    print("\n=== 🧾 FINAL TRANSACTION RECEIPT (Rail Event Log) ===")
    for ev in event_log:
        ev_dict = normalise_event(ev)
        print(json.dumps(ev_dict, indent=2))


def generate_evidence_capsule(transaction_id, event_log, audit_chain):
    """Build and persist a Cloked Evidence Capsule from a transaction run."""
    print("\n📦 GENERATING EVIDENCE CAPSULE...\n")

    # Convert all events to plain dicts for the capsule
    event_dicts = [normalise_event(ev) for ev in event_log]

    capsule = EvidenceCapsule(
        capsule_id=str(uuid.uuid4()),
        transaction_id=transaction_id,
        generated_at=datetime.utcnow().isoformat() + "Z",
        schema_version="1.0",
        events=event_dicts,
        audit_hash=audit_chain.get_final_hash(),
    )

    capsule_json = capsule.to_json()
    print(capsule_json)

    # Optional: write to disk
    filename = f"evidence_capsule_{transaction_id}.json"
    capsule.save_to_disk(filename)

    return capsule


def run_transaction_scenario():
    """
    Run a single happy-path transaction through Aiva → Rail.

    Returns:
        final_state: Enum or string representing the final state.
        event_log: list of RailEvent objects (or dicts).
        transaction_id: unique ID for this run.
    """
    route_engine = RouteEngine()
    route = route_engine.get_best_route(origin="NodeA", destination="NodeB")

    print("\n🧠 AIVA Selected Route:", route)

    rail_exec = RailExecutor()
    final_state, event_log = rail_exec.execute_transaction(route)

    transaction_id = str(uuid.uuid4())
    return final_state, event_log, transaction_id


def main():
    print("\n🚀 Starting Lupine Systems Walking Skeleton\n")

    final_state, event_log, transaction_id = run_transaction_scenario()

    # Handle both Enum and simple string states safely
    state_name = getattr(final_state, "name", final_state)
    print("\n=== RAIL FINAL STATE ===")
    print("State:", state_name)

    # 1) Show Rail event log (now safely serialisable)
    print_event_log(event_log)

    # 2) Build Cloked audit chain from events
    print("\n🔐 Building Cloked Audit Chain...\n")
    audit_chain = AuditChain()
    for ev in event_log:
        ev_dict = normalise_event(ev)
        audit_chain.log_event(ev_dict)

    print("=== CLOKED: Integrity Check (Before Tamper) ===")
    print("Integrity OK?", audit_chain.verify_integrity())

    # 3) Tamper test to prove chain detects modification
    print("\n⚠️ Tampering with chain for verification test...\n")
    if len(audit_chain.chain) > 1:
        # Flip something small in the first real event
        audit_chain.chain[1]["event"]["event_type"] = "TAMPERED_DATA"

    print("=== CLOKED: Integrity Check (After Tamper) ===")
    print("Integrity OK?", audit_chain.verify_integrity())

    # 4) Generate final Evidence Capsule
    generate_evidence_capsule(
        transaction_id=transaction_id,
        event_log=event_log,
        audit_chain=audit_chain,
    )

    print("\n🏁 End of Transaction\n")


if __name__ == "__main__":
    main()
