import uuid
import json
from datetime import datetime


class EvidenceCapsule:
    def __init__(self, capsule_id, transaction_id, generated_at,
                 schema_version, events, audit_hash):
        self.capsule_id = capsule_id
        self.transaction_id = transaction_id
        self.generated_at = generated_at
        self.schema_version = schema_version
        self.events = events
        self.audit_hash = audit_hash

    def to_dict(self):
        return {
            "capsule_id": self.capsule_id,
            "transaction_id": self.transaction_id,
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "audit_hash": self.audit_hash,
            "events": self.events
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def save_to_disk(self, filename):
        with open(filename, "w") as f:
            f.write(self.to_json())
