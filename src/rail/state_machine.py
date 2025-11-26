# src/rail/state_machine.py

from enum import Enum


class TransactionState(str, Enum):
    """
    Simple transaction lifecycle states for the Lupine Rail layer.

    INIT      → transaction created, not yet moving
    MOVING    → actively executing hops along the route
    COMPLETED → all hops executed successfully
    FAILED    → one or more hops failed
    """

    INIT = "INIT"
    MOVING = "MOVING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

