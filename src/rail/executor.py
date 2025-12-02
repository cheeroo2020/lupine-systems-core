# src/rail/executor.py

from __future__ import annotations

import random
import time
from typing import List

from src.rail.state_machine import TransactionState


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
    """

    def __init__(self) -> None:
        self.state: TransactionState = TransactionState.CREATED

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
            try:
                print(
                    f">>> RAIL: Executing hop to {node} "
                    f"(attempt {attempt}/{MAX_RETRIES})..."
                )
                # Chaos Monkey: 25% chance of simulated network failure
                if random.random() < 0.25:
                    raise ConnectionError("Bank API Offline")

                # If we reach here, the hop "succeeded"
                return True

            except ConnectionError as exc:
                if attempt < MAX_RETRIES:
                    print(
                        f"⚠️  Network Glitch. Retrying hop to {node} "
                        f"(Attempt {attempt + 1}/{MAX_RETRIES})... "
                        f"Reason: {exc}"
                    )
                    time.sleep(1.0)  # backoff simulation
                else:
                    print(
                        f"✖ RAIL: Hop to {node} failed after "
                        f"{MAX_RETRIES} attempts. Error: {exc}"
                    )
                    return False

        # Should never reach here, but keep for completeness
        return False

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
        if not route:
            # No route to execute – treat as rejected/misconfigured.
            self.state = TransactionState.AIVA_REJECTED
            print(">>> RAIL: No route provided, marking as AIVA_REJECTED.")
            return self.state

        # Assume Aiva has already run risk checks before calling Rail.
        self.state = TransactionState.LIQUIDITY_LOCKED
        print(f">>> RAIL: Liquidity locked for route: {route}")

        self.state = TransactionState.IN_FLIGHT
        for node in route:
            hop_success = self._execute_hop_with_retries(node)
            if not hop_success:
                # Transition to FAILED and stop processing further hops.
                self.state = TransactionState.FAILED
                print(">>> RAIL: TRANSACTION FAILED due to network instability.")
                return self.state

        self.state = TransactionState.SETTLED
        print(">>> RAIL: Transaction settled successfully.")

        return self.state
