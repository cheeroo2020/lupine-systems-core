# src/aiva/mock_graphs.py

class MedicalGraph:
    """
    Mock Medical Graph for Aiva v0.1 walking skeleton.
    For now, this graph provides a constant score for any node.
    """

    def __init__(self):
        # placeholder data structure
        self.nodes = []

    def get_score(self, node):
        """
        Return a constant score for now (Phase 1 walking skeleton).
        """
        return 1.0


class VolatilityGraph:
    """
    Mock Volatility Graph for Aiva v0.1 walking skeleton.
    For now, this graph provides a constant score for any node.
    """

    def __init__(self):
        # placeholder data structure
        self.nodes = []

    def get_score(self, node):
        """
        Return a constant score for now (Phase 1 walking skeleton).
        """
        return 1.0
