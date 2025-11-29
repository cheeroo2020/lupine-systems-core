# src/aiva/compliance_graph.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List


BLACKLIST: List[str] = ["North Korea", "Iran"]
HIGH_RISK_THRESHOLD: float = 0.8  # reserved for future use


@dataclass(frozen=True)
class ComplianceContext:
    """
    Minimal compliance context for early Aiva gating.

    For now we use:
    - destination_country: where funds/benefit ultimately land
    - beneficiary_id: opaque identifier (account, entity, customer)
    """
    destination_country: str
    beneficiary_id: str


class ComplianceGraph:
    """
    Compliance risk engine for Aiva v0.1.

    Rules (walking-skeleton version):

    - If destination_country is in BLACKLIST →
        score = 0.0  (hard reject: sanctions violation)

    - If destination_country == "High Risk" →
        score = 0.5  (requires manual review, not auto-approvable)

    - Otherwise →
        score = 1.0  (no elevated jurisdictional risk detected)
    """

    def get_compliance_score(self, ctx: ComplianceContext) -> float:
        """
        Compute a simple compliance score for the given corridor.

        Parameters
        ----------
        ctx : ComplianceContext
            Destination country + beneficiary id.

        Returns
        -------
        float
            Compliance score in [0.0, 1.0].
            - 0.0 → hard reject (sanctions / prohibited)
            - 0.5 → high risk (manual review required)
            - 1.0 → clear from this simple jurisdiction check
        """
        country = ctx.destination_country

        # Hard sanctions / prohibited list
        if country in BLACKLIST:
            return 0.0

        # Mock "high risk" classification for now
        if country == "High Risk":
            return 0.5

        # Otherwise, treat as safe in this minimal model
        return 1.0


if __name__ == "__main__":
    graph = ComplianceGraph()

    safe_ctx = ComplianceContext(destination_country="Singapore", beneficiary_id="BEN-123")
    high_risk_ctx = ComplianceContext(destination_country="High Risk", beneficiary_id="BEN-999")
    blocked_ctx = ComplianceContext(destination_country="North Korea", beneficiary_id="BEN-SDNTK")

    print("Singapore:", graph.get_compliance_score(safe_ctx))      # expect 1.0
    print("High Risk:", graph.get_compliance_score(high_risk_ctx)) # expect 0.5
    print("North Korea:", graph.get_compliance_score(blocked_ctx)) # expect 0.0

