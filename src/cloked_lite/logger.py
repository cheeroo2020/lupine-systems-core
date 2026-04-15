"""
Cloked-lite Logger — cryptographic evidence chain.
From P4-Ch1/Ch4: hash → anchor → verify, evidence capsules.

Every event is hashed and chained to the previous entry,
creating an immutable, verifiable audit trail.
"""
import hashlib
import json
from src.models.schemas import EvidenceLog, EvidenceEntry


def _hash_data(data: dict) -> str:
    """SHA-256 hash of event data."""
    serialised = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(serialised.encode()).hexdigest()


def create_evidence_log(request_id: str) -> EvidenceLog:
    """Create a new evidence log for a movement request."""
    return EvidenceLog(request_id=request_id)


def append_evidence(
    log: EvidenceLog,
    event_type: str,
    payload: dict,
) -> EvidenceLog:
    """
    Append an evidence entry to the chain.
    Each entry is hashed and linked to the previous entry's hash.
    """
    sequence = len(log.entries)
    previous_hash = log.entries[-1].data_hash if log.entries else "genesis"

    data_hash = _hash_data({
        "sequence": sequence,
        "event_type": event_type,
        "previous_hash": previous_hash,
        "payload": payload,
    })

    entry = EvidenceEntry(
        sequence=sequence,
        event_type=event_type,
        data_hash=data_hash,
        previous_hash=previous_hash,
        payload=payload,
    )

    log.entries.append(entry)
    return log


def verify_chain(log: EvidenceLog) -> bool:
    """
    Verify the integrity of the evidence chain.
    Each entry's hash must match its recomputed hash,
    and previous_hash must match the prior entry.
    """
    for i, entry in enumerate(log.entries):
        # Check chain linkage
        expected_prev = log.entries[i - 1].data_hash if i > 0 else "genesis"
        if entry.previous_hash != expected_prev:
            return False

        # Verify hash
        recomputed = _hash_data({
            "sequence": entry.sequence,
            "event_type": entry.event_type,
            "previous_hash": entry.previous_hash,
            "payload": entry.payload,
        })
        if entry.data_hash != recomputed:
            return False

    return True
