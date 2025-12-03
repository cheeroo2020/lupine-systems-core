# src/rail/executor.py

from __future__ import annotations

import json
import random
import time
from typing import List

from src.rail.state_machine import TransactionState
from src.rail.events import RailEvent, RailEventType


MAX_RETRIES: int = 3  # Story 4.3 – Failover & Retry Logic


class RailExecutor:
    """
    Executes a route produced by Aiva across Lupine Rail.

    Lifecycle (simplified):
    - Starts at CREATED
    - (Assume Aiva checks already passed before this call)
    - Locks liquidity
    - Moves through hops with retry/failover logic
    - Ends at SETTLED or FAILED

    All side effects are emitted as structured RailEvent objects.
    """

    def __init__(self) -> None:
        self.state: TransactionState = TransactionState.CREATED
        self.event_log: List[RailEvent] = []

    # ---------- Event helper ----------

    def _emit_event(self, event_type: RailEventType, details: dict) -> None:
        event = RailEvent.create(event_type=event_type, details=details)
        self.event_log.append(event)
        # Print structured JSON line (JSON-ready logs)
        print(json.dumps(event.to_dict(), ensure_ascii=False))

    # ---------- Hop execution with retry ----------

    def _execute_hop_with_retries(self, node: str) -> bool:
        """
        Execute a single hop with retry logic and simulated network failures.

        Simulated Chaos:
        - On each attempt, there's a 25% chance of ConnectionError
          (e.g., "Bank API Offline").

        Returns
        -------
        bool
            True if hop eventually succeeded within MAX_RETRIES,
            False if all retries failed.
        """
        for attempt in range(1, MAX_RETRIES + 1):
            # Hop attempt event
            self._emit_event(
                RailEventType.HOP_ATTEMPT,
                {
                    "node_id": node,
                    "attempt": attempt,
                    "max_retries": MAX_RETRIES,
                },
            )

            try:
                # Chaos Monkey: 25% chance of simulated network failure
                if random.random() < 0.25:
                    raise ConnectionError("Bank API Offline")

                # Hop succeeded
                self._emit_event(
                    RailEventType.HOP_SUCCESS,
                    {
                        "node_id": node,
                        "attempt": attempt,
                    },
                )
                return True

            except ConnectionError as exc:
                # Failure / retry event
                will_retry = attempt < MAX_RETRIES
                self._emit_event(
                    RailEventType.HOP_FAILURE,
                    {
                        "node_id": node,
                        "attempt": attempt,
                        "max_retries": MAX_RETRIES,
                        "reason": str(exc),
                        "will_retry": will_retry,
                    },
                )

                if will_retry:
                    time.sleep(1.0)  # backoff simulation
                else:
                    # All retries exhausted
                    return False

        # Should never hit, but keep for completeness
        return False

    # ---------- Public API ----------

    def execute_transaction(self, route: List[str]) -> TransactionState:
        """
        Execute a transaction along the given route.

        Parameters
        ----------
        route : List[str]
            Sequence of node identifiers (hops).

        Returns
        -------
        TransactionState
            Final state (expected: SETTLED on success, FAILED on repeated errors).
        """
        # Transaction start event
        self._emit_event(
            RailEventType.TRANSACTION_START,
            {
                "route": route,
            },
        )

        if not route:
            # No route to execute – treat as rejected/misconfigured.
            self.state = TransactionState.AIVA_REJECTED
            self._emit_event(
                RailEventType.TRANSACTION_COMPLETE,
                {
                    "status": "AIVA_REJECTED",
                    "state": self.state.name,
                    "code": self.state.value,
                    "reason": "No route provided",
                },
            )
            return self.state

        # Assume Aiva has already run risk checks before calling Rail.
        self.state = TransactionState.LIQUIDITY_LOCKED
        self._emit_event(
            RailEventType.TRANSACTION_START,
            {
                "status": "LIQUIDITY_LOCKED",
                "route": route,
            },
        )

        self.state = TransactionState.IN_FLIGHT
        for node in route:
            hop_success = self._execute_hop_with_retries(node)
            if not hop_success:
                # Transition to FAILED and stop processing further hops.
                self.state = TransactionState.FAILED
                self._emit_event(
                    RailEventType.TRANSACTION_COMPLETE,
                    {
                        "status": "FAILED",
                        "state": self.state.name,
                        "code": self.state.value,
                        "route": route,
                        "reason": "Network instability / max retries exceeded",
                    },
                )
                return self.state

        self.state = TransactionState.SETTLED
        self._emit_event(
            RailEventType.TRANSACTION_COMPLETE,
            {
                "status": "SETTLED",
                "state": self.state.name,
                "code": self.state.value,
                "route": route,
            },
        )

        return self.state
