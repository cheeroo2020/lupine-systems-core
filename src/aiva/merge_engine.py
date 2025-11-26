# src/aiva/merge_engine.py

from .hop_graph import build_hop_graph
from .mock_graphs import MedicalGraph, VolatilityGraph


class MergeEngine:
    """
    Walking Skeleton Merge Engine for Aiva v0.1.
    This version does NOT compute real routes yet.
    It simply wires together the components to validate integration.
    """

    def __init__(self):
        # Load the Hop Graph from your existing implementation
        self.hop_graph = build_hop_graph()

        # Instantiate mock graphs
        self.medical_graph = MedicalGraph()
        self.volatility_graph = VolatilityGraph()

    def get_best_route(self, start, end):
        """
        Mock route finder.
        In the real version, this will merge multi-graph weights,
        compute candidate routes, apply scoring, and extract the
        Pareto frontier.
        
        For now: return a hard-coded route to test the pipeline.
        """
        return [start, end]

    def get_mock_scores(self, node):
        """
        Returns mock scores aggregated from the mock graphs.
        This is purely for testing the full pipeline.
        """
        med_score = self.medical_graph.get_score(node)
        vol_score = self.volatility_graph.get_score(node)

        return {
            "medical": med_score,
            "volatility": vol_score
        }


if __name__ == "__main__":
    # Manual test
    engine = MergeEngine()
    route = engine.get_best_route("NodeA", "NodeB")
    print("Mock route:", route)

    scores = engine.get_mock_scores("NodeA")
    print("Mock scores:", scores)

