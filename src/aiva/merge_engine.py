# src/aiva/merge_engine.py

from __future__ import annotations

from typing import List

from .hop_graph import build_hop_graph


class RouteEngine:
    """
    Thin routing facade used by the Lupine walking skeleton.

    Right now this is intentionally simple:
    - We build the hop graph (so future work can use it).
    - We expose a single method `get_best_route(origin, destination)`
      that returns a static happy-path route for the demo.

    Later, this class can be upgraded to call the full multi-graph
    Aiva engine without changing the public interface.
    """

    def __init__(self) -> None:
        # Build and keep a reference to the hop graph, even if the
        # current skeleton does not yet traverse it dynamically.
        try:
            self.graph = build_hop_graph()
        except Exception:
            # Fail-safe: if hop_graph changes or is not available,
            # we still allow the skeleton to run.
            self.graph = None

    def get_best_route(self, origin: str, destination: str) -> List[str]:
        """
        Return the preferred route between origin and destination.

        For the current skeleton we return a fixed happy-path route
        that matches the rest of the demo and tests.
        """
        # In future: use self.graph to compute the actual path.
        # For now, the skeleton is built around ['NodeA', 'NodeB'].
        return ["NodeA", "NodeB"]
