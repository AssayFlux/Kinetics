"""Storage backends for Kinetics.

SQLite is used for metadata, provenance, indexes, and workflow state.
Large scientific arrays and model checkpoints belong in file/object storage.
"""

from kinetics_core.storage.sqlite_store import KineticsSQLite

__all__ = ["KineticsSQLite"]
