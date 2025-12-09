import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List


class ClokedLogger:
    """
    Legacy simple logger (still here in case you use it elsewhere).
    Not used by the new audit chain, but harmless to keep.
    """

    def log_event(self, source: str, message: str) -> str:
        payload = f"{source}|{message}"
        hash_value = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        print(
            f"🔒 CLOKED EVIDENCE: [{source}] {message} | Hash: {hash_value}"
        )
        return hash_value


class AuditChain:
    """
    AuditChain
    ----------
    Blockchain-style hash chain for Rail events.

    Each entry links:
      prev_hash + event_json  ->  sha256 -> current hash
    """

    def __init__(self) -> None:
        self.chain: List[Dict[str, Any]] = []

        # Genesis block with a fixed previous_hash
        genesis_prev = "0" * 64
        genesis_event = {
            "event_id": "GENESIS",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "GENESIS",
            "details": {},
        }
        genesis_hash = self._compute_hash(genesis_prev, genesis_event)
        self.chain.append(
            {
                "event": genesis_event,
                "hash": genesis_hash,
                "previous_hash": genesis_prev,
            }
        )

    # ----------------- internal helpers -----------------

    def _compute_hash(
        self, previous_hash: str, event: Dict[str, Any]
    ) -> str:
        event_str = json.dumps(event, sort_keys=True, separators=(",", ":"))
        payload = (previous_hash + event_str).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    # ----------------- public API -----------------

    def log_event(self, event: Dict[str, Any]) -> None:
        """
        Append an event to the chain and compute a new tip hash.
        """
        previous_hash = self.chain[-1]["hash"] if self.chain else "0" * 64
        new_hash = self._compute_hash(previous_hash, event)
        entry = {
            "event": event,
            "hash": new_hash,
            "previous_hash": previous_hash,
        }
        self.chain.append(entry)

    def verify_integrity(self) -> bool:
        """
        Walk the chain and recompute each hash.

        Returns False if any entry has been tampered with.
        """
        if not self.chain:
            return True

        for i, entry in enumerate(self.chain):
            if i == 0:
                # Genesis is assumed correct
                continue

            prev_hash = self.chain[i - 1]["hash"]
            event = entry["event"]
            expected_hash = self._compute_hash(prev_hash, event)

            if expected_hash != entry["hash"]:
                return False

        return True

    def get_final_hash(self) -> str:
        """
        Return the current tip hash of the chain (for EvidenceCapsule).
        """
        if not self.chain:
            return ""
        return self.chain[-1]["hash"]
