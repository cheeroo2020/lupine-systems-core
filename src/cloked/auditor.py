# src/cloked/auditor.py

import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Union


class ClokedLogger:
    """
    Simple hash-printing logger (existing behaviour, kept for compatibility).
    """
    @staticmethod
    def log_event(source: str, message: str) -> None:
        payload = f"[{source}] {message}"
        hash_value = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        print(
            f"🔒 CLOKED EVIDENCE: {payload} | Hash: {hash_value}"
        )


class AuditChain:
    """
    Cryptographic event chain (Story 5.1).

    - Maintains an append-only list of entries.
    - Each entry links to the previous via SHA-256(previous_hash + event_json).
    - verify_integrity() recomputes all hashes and returns False if any mismatch.
    """

    def __init__(self) -> None:
        self.chain: List[Dict[str, Any]] = []
        self._init_genesis_block()

    def _init_genesis_block(self) -> None:
        """
        Create the genesis block with a fixed previous_hash.
        """
        previous_hash = "0" * 64
        event = {
            "type": "GENESIS",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        event_str = json.dumps(event, sort_keys=True)
        block_hash = hashlib.sha256(
            (previous_hash + event_str).encode("utf-8")
        ).hexdigest()

        genesis_entry = {
            "event": event,
            "previous_hash": previous_hash,
            "hash": block_hash,
        }
        self.chain.append(genesis_entry)

    def log_event(self, event: Union[Dict[str, Any], Any]) -> None:
        """
        Append a new event to the chain.

        Accepts a dict or an object with a .to_dict() method (e.g. RailEvent).
        """
        if hasattr(event, "to_dict"):
            event_dict = event.to_dict()
        else:
            event_dict = dict(event)

        previous_hash = self.chain[-1]["hash"] if self.chain else "0" * 64
        event_str = json.dumps(event_dict, sort_keys=True)
        block_hash = hashlib.sha256(
            (previous_hash + event_str).encode("utf-8")
        ).hexdigest()

        entry = {
            "event": event_dict,
            "previous_hash": previous_hash,
            "hash": block_hash,
        }
        self.chain.append(entry)

    def verify_integrity(self) -> bool:
        """
        Recompute all hashes and check links.

        Returns:
            True  -> chain is consistent
            False -> at least one entry was tampered with
        """
        if not self.chain:
            return True

        for idx, entry in enumerate(self.chain):
            expected_prev = "0" * 64 if idx == 0 else self.chain[idx - 1]["hash"]

            # Check that stored previous_hash matches
            if entry["previous_hash"] != expected_prev:
                return False

            # Recompute hash from stored event + expected_prev
            event_str = json.dumps(entry["event"], sort_keys=True)
            expected_hash = hashlib.sha256(
                (expected_prev + event_str).encode("utf-8")
            ).hexdigest()

            if entry["hash"] != expected_hash:
                return False

        return True
