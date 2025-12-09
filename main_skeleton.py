import json
from typing import Any, Dict

from src.aiva.merge_engine import RouteEngine
from src.rail.executor import RailExecutor
from src.cloked.auditor import ClokedLogger, AuditChain


def _event_to_dict(ev: Any) -> Dict[str, Any]:
    """
    Helper: normalise a RailEvent or plain dict into a dict.
    """
    if hasattr(ev, "to_dict"):
        return ev.to_dict()  # RailEvent
    if isinstance(ev, dict):
        return ev
    # Fallback – best-effort conversion
    return dict(ev)


def run_transaction_scenario() -> None:
    print("\n🚀 Starting Lupine Systems Walking Skeleton\n")

    # === AIVA: Determine Best Route ===
    engine = RouteEngine()
    route = engine.get_best_route("Sydney", "Singapore")
    print("🧠 AIVA Selected Route:", route)

    # === RAIL: Execute Transaction ===
    executor = RailExecutor()

    # NOTE: executor returns (final_state_str, event_log)
    final_state, event_log = executor.execute_transaction(route)

    print("\n=== RAIL FINAL STATE ===")
    # final_state is a string, so we print it directly
    print(f"State: {final_state}")

    # === RAIL: Structured JSON Event Summary ===
    print("\n=== 🧾 FINAL TRANSACTION RECEIPT (Rail Event Log) ===")
    normalised_events = [_event_to_dict(ev) for ev in event_log]
    for ev_dict in normalised_events:
        print(json.dumps(ev_dict, indent=2))

    # === CLOKED: Hash-linked Audit Chain ===
    print("\n🔐 Building Cloked Audit Chain...")
    audit_chain = AuditChain()

    # Feed each RailEvent (as dict) into the Cloked chain
    for ev_dict in normalised_events:
        audit_chain.log_event(ev_dict)

    # === Integrity Check BEFORE any tampering ===
    print("\n=== CLOKED: Integrity Check (Before Tamper) ===")
    print("Integrity OK?", audit_chain.verify_integrity())

    # === DELIBERATE TAMPER TEST ===
    print("\n⚠️  Tampering with chain for verification test...")
    if len(audit_chain.chain) > 1:
        entry = audit_chain.chain[1]
        event_payload = entry.get("event")

        # If the event is a dict, mutate that; otherwise, set an attribute.
        if isinstance(event_payload, dict):
            event_payload["amount"] = 99_999_999
        else:
            setattr(event_payload, "amount", 99_999_999)

    # === Integrity Check AFTER tampering ===
    print("\n=== CLOKED: Integrity Check (After Tamper) ===")
    print("Integrity OK?", audit_chain.verify_integrity())

    print("\n🏁 End of Transaction\n")


if __name__ == "__main__":
    run_transaction_scenario()
