from dataclasses import dataclass
from pathlib import Path
import yaml
from .connection import KuzuConnection
from .schema import initialize

@dataclass
class FederatedGraphs:
    ontology: KuzuConnection
    semantic: KuzuConnection
    metadata: KuzuConnection

    @classmethod
    def from_config(cls, config):
        paths=config["graph"]
        ontology=initialize(paths["ontology_database_path"], "ontology")
        semantic=initialize(paths["semantic_database_path"], "semantic")
        metadata=initialize(paths["metadata_database_path"], "metadata")
        return cls(ontology, semantic, metadata)
