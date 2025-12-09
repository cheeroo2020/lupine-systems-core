import json
from src.aiva.merge_engine import RouteEngine
from src.rail.executor import RailExecutor
from src.cloked.auditor import ClokedLogger, AuditChain


def run_transaction_scenario():
    print("\n🚀 Starting Lupine Systems Walking Skeleton\n")

    # === AIVA: Determine Best Route ===
    engine = RouteEngine()
    route = engine.get_best_route("Sydney", "Singapore")
    print("\n🧠 AIVA Selected Route:", route)

    # === RAIL: Execute Transaction ===
    executor = RailExecutor()

    final_state, event_log = executor.execute_transaction(route)

    print("\n=== RAIL FINAL STATE ===")
    print(f"State: {final_state.name}  (code={final_state.value})")

    # === RAIL: Structured JSON Event Summary ===
    print("\n=== 🧾 FINAL TRANSACTION RECEIPT (Rail Event Log) ===")
    for ev in event_log:
        print(json.dumps(ev.to_dict(), indent=2))

    # === CLOKED: Hash-linked Audit Chain ===
    print("\n🔐 Building Cloked Audit Chain...")
    audit_chain = AuditChain()

    # Feed each RailEvent into the Cloked chain
    for ev in event_log:
        audit_chain.log_event(ev)

    # === Integrity Check BEFORE any tampering ===
    print("\n=== CLOKED: Integrity Check (Before Tamper) ===")
    print("Integrity OK?", audit_chain.verify_integrity())

    # === DELIBERATE TAMPER TEST ===
    print("\n⚠️  Tampering with chain for verification test...")
    if len(audit_chain.chain) > 1:
        # Tamper with the FIRST non-genesis entry
        try:
            audit_chain.chain[1]["event"]["amount"] = 99999999
        except Exception:
            # If event didn’t have an amount field, add one
            audit_chain.chain[1]["event"]["amount"] = 99999999

    # === Integrity Check AFTER tampering ===
    print("\n=== CLOKED: Integrity Check (After Tamper) ===")
    print("Integrity OK?", audit_chain.verify_integrity())

    print("\n🏁 End of Transaction\n")


if __name__ == "__main__":
    run_transaction_scenario()
