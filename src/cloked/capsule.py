import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class EvidenceCapsule:
    """
    EvidenceCapsule
    ----------------
    A portable, sealed container for a single transaction's history.

    This is what Lupine would hand to a regulator or auditor:
      - who moved value
      - how it moved (Rail events)
      - what the final audit hash was (Cloked chain tip)
    """

    capsule_id: str
    transaction_id: str
    schema_version: str
    generated_at: str
    events: List[Dict[str, Any]]
    audit_hash: str

    @classmethod
    def create(
        cls,
        transaction_id: str,
        events: List[Dict[str, Any]],
        audit_hash: str,
        schema_version: str = "1.0",
    ) -> "EvidenceCapsule":
        """Factory helper to build a new capsule with fresh IDs + timestamps."""
        capsule_id = str(uuid.uuid4())
        generated_at = datetime.now(timezone.utc).isoformat()
        return cls(
            capsule_id=capsule_id,
            transaction_id=transaction_id,
            schema_version=schema_version,
            generated_at=generated_at,
            events=events,
            audit_hash=audit_hash,
        )

    def to_json(self) -> str:
        """Return a pretty-printed JSON representation of the capsule."""
        data = asdict(self)
        return json.dumps(data, indent=2, ensure_ascii=False)

    def save_to_disk(self, filename: str) -> None:
        """Persist the capsule JSON to disk."""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.to_json())
