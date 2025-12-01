# src/rail/state_machine.py

from __future__ import annotations

from enum import Enum


class TransactionState(Enum):
    """
    Transaction lifecycle for Lupine Rail.

    New model:
    - CREATED (100)
    - AIVA_CHECKING (200)
    - AIVA_REJECTED (400)
    - LIQUIDITY_LOCKED (300)
    - IN_FLIGHT (500)
    - SETTLED (600)

    Backwards-compatibility aliases:
    - INIT      -> CREATED
    - MOVING    -> IN_FLIGHT
    - COMPLETED -> SETTLED
    - FAILED    -> AIVA_REJECTED
    """

    CREATED = 100
    AIVA_CHECKING = 200
    AIVA_REJECTED = 400
    LIQUIDITY_LOCKED = 300
    IN_FLIGHT = 500
    SETTLED = 600

    # Aliases so older code using INIT/MOVING/etc does not break
    INIT = 100
    MOVING = 500
    COMPLETED = 600
    FAILED = 400
