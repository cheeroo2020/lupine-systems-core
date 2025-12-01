# src/rail/executor.py

from __future__ import annotations

from typing import List

from src.rail.state_machine import TransactionState


class RailExecutor:
    """
    Executes a route produced by Aiva across Lupine Rail.

    For now:
    - Starts at CREATED
    - (Assume Aiva checks already passed)
    - Locks liquidity
    - Moves through hops
    - Ends at SETTLED
    """

    def __init__(self) -> None:
        self.state: TransactionState = TransactionState.CREATED

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
            Final state (expected: SETTLED in this simple skeleton).
        """
        if not route:
            # No route to execute – treat as rejected/misconfigured.
            self.state = TransactionState.AIVA_REJECTED
            print(">>> RAIL: No route provided, marking as AIVA_REJECTED.")
            return self.state

        # Assume Aiva already ran risk checks before we get here.
        self.state = TransactionState.LIQUIDITY_LOCKED
        print(f">>> RAIL: Liquidity locked for route: {route}")

        self.state = TransactionState.IN_FLIGHT
        for node in route:
            print(f">>> RAIL: Executing hop to {node}...")

        self.state = TransactionState.SETTLED
        print(">>> RAIL: Transaction settled successfully.")

        return self.state
