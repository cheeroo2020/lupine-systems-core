# src/aiva/liquidity_graph.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


# Mock "balance sheet" for key nodes in the network.
MOCK_NODE_BALANCES: Dict[str, float] = {
    "Bank_Sydney": 1_000_000.00,
    "Bank_Singapore": 50_000.00,
}


LIQUIDITY_STRESS_THRESHOLD: float = 0.8  # 80 percent of balance


@dataclass(frozen=True)
class LiquidityContext:
    """
    Minimal context for evaluating liquidity at a settlement node.

    Attributes
    ----------
    node_id : str
        Identifier of the node (bank, PSP, hub) whose balance we check.
    transaction_amount : float
        Amount required to be settled at this node.
    """
    node_id: str
    transaction_amount: float


class LiquidityGraph:
    """
    Simple liquidity risk model for Aiva v0.1.

    Rules
    -----
    - If transaction_amount > node_balance:
        score = 0.0   (insufficient liquidity, hard reject)
    - If transaction_amount is between 80 percent and 100 percent of balance:
        score = 0.5   (high stress; not suitable for automated routing)
    - Otherwise:
        score = 1.0   (healthy liquidity headroom)
    """

    def get_liquidity_score(self, ctx: LiquidityContext) -> float:
        """
        Compute a liquidity score for the given node.

        Parameters
        ----------
        ctx : LiquidityContext
            Node identifier and requested transaction amount.

        Returns
        -------
        float
            Liquidity score in [0.0, 1.0].
        """
        node_id = ctx.node_id
        amount = ctx.transaction_amount

        balance = MOCK_NODE_BALANCES.get(node_id)

        # Unknown node: treat as zero balance for now.
        if balance is None:
            return 0.0

        # Hard reject: not enough funds.
        if amount > balance:
            return 0.0

        # Negative or zero amounts are trivially safe.
        if amount <= 0:
            return 1.0

        # Check stress zone (80%+ of available balance).
        utilisation_ratio = amount / balance
        if utilisation_ratio >= LIQUIDITY_STRESS_THRESHOLD:
            return 0.5

        # Otherwise assume healthy.
        return 1.0


if __name__ == "__main__":
    graph = LiquidityGraph()

    small = LiquidityContext("Bank_Singapore", 10_000.0)
    stressed = LiquidityContext("Bank_Singapore", 42_000.0)
    busted = LiquidityContext("Bank_Singapore", 75_000.0)

    print("Small:", graph.get_liquidity_score(small))      # expect 1.0
    print("Stressed:", graph.get_liquidity_score(stressed))  # expect 0.5
    print("Busted:", graph.get_liquidity_score(busted))    # expect 0.0

