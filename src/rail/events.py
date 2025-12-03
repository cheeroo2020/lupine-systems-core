# src/rail/events.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
from uuid import uuid4


class RailEventType(Enum):
    TRANSACTION_START = "TRANSACTION_START"
    HOP_ATTEMPT = "HOP_ATTEMPT"
    HOP_SUCCESS = "HOP_SUCCESS"
    HOP_FAILURE = "HOP_FAILURE"
    TRANSACTION_COMPLETE = "TRANSACTION_COMPLETE"


@dataclass
class RailEvent:
    event_id: str
    timestamp: str
    event_type: RailEventType
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, event_type: RailEventType, details: Dict[str, Any]) -> "RailEvent":
        return cls(
            event_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            details=details or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type.name,
            "details": self.details,
        }

