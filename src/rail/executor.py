# src/rail/executor.py

from typing import List
from .state_machine import TransactionState


class RailExecutor:
    """
    Minimal execution layer for Lupine Rail.

    This is a walking-skeleton executor that:
    - accepts a route (list of nodes)
    - iterates over each hop
    - prints execution logs
    - returns a final transaction state as a string
    """

    def __init__(self) -> None:
        self.state: TransactionState = TransactionState.INIT

    def execute_transaction(self, route: List[str]) -> str:
        """
        Execute a transaction along the given route.

        Parameters
        ----------
        route : List[str]
            The ordered list of nodes Aiva has chosen for this transaction.

        Returns
        -------
        str
            "COMPLETED" if the execution finishes successfully.
            (Future versions may return other states on failure.)
        """
        if not route:
            # No route → immediately fail
            self.state = TransactionState.FAILED
            return self.state.value

        # Transition to MOVING
        self.state = TransactionState.MOVING

        for node in route:
            print(f">>> RAIL: Executing hop to {node}...")

            # Walking skeleton: assume every hop succeeds.
            # Later, we will inject failure probabilities, latency, etc.

        # If we completed the loop without issues:
        self.state = TransactionState.COMPLETED
        return self.state.value


if __name__ == "__main__":
    # Simple manual test for the walking skeleton
    executor = RailExecutor()
    sample_route = ["NodeA", "NodeB", "NodeC"]
    final_state = executor.execute_transaction(sample_route)
    print(f"Final transaction state: {final_state}")
