# src/cloked/auditor.py

import hashlib
from typing import Any


class ClokedLogger:
    """
    Minimal audit logger for the Cloked evidence layer.

    This walking-skeleton version:
    - accepts a source (module name, hop, subsystem, etc.)
    - accepts a message (event text)
    - computes a SHA-256 hash of the message
    - prints a verifiable audit line
    """

    def log_event(self, source: str, message: str) -> None:
        """
        Log an audit event with a SHA-256 hash.

        Parameters
        ----------
        source : str
            The source subsystem or component (e.g., "AIVA", "RAIL", "MERGE_ENGINE").

        message : str
            The human-readable event message to be hashed.
        """
        # SHA-256 hashing
        hash_value = hashlib.sha256(message.encode("utf-8")).hexdigest()

        print(
            f"🔒 CLOKED EVIDENCE: [{source}] {message} | Hash: {hash_value}"
        )


if __name__ == "__main__":
    logger = ClokedLogger()
    logger.log_event("TEST", "Sample audit event generated.")
