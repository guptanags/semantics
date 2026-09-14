from __future__ import annotations

import argparse
from .connection import KuzuConnection

ONTOLOGY_DDL = [
"""CREATE NODE TABLE IF NOT EXISTS Concept(id STRING PRIMARY KEY, name STRING, concept_type STRING, domain STRING, definition STRING, status STRING, version STRING)""",
"""CREATE NODE TABLE IF NOT EXISTS ConceptType(id STRING PRIMARY KEY, name STRING)""",
"""CREATE NODE TABLE IF NOT EXISTS RelationshipType(id STRING PRIMARY KEY, name STRING, inverse_type STRING, domain_concept_type STRING, range_concept_type STRING, transitive BOOLEAN, symmetric BOOLEAN, temporal BOOLEAN, resolution_priority INT64, status STRING, version STRING)""",
"""CREATE NODE TABLE IF NOT EXISTS RelationshipAssertion(id STRING PRIMARY KEY, relationship_type_id STRING, source_id STRING, target_id STRING, valid_from STRING, valid_to STRING, asserted_at STRING, confidence DOUBLE, approval_status STRING, source_system STRING, source_reference STRING, ontology_version STRING)""",
"""CREATE NODE TABLE IF NOT EXISTS SemanticRole(id STRING PRIMARY KEY, name STRING, description STRING)""",
"""CREATE NODE TABLE IF NOT EXISTS Synonym(id STRING PRIMARY KEY, text STRING, language STRING)""",
"""CREATE NODE TABLE IF NOT EXISTS ExternalMapping(id STRING PRIMARY KEY, system STRING, external_id STRING, mapping_type STRING)""",
"""CREATE NODE TABLE IF NOT EXISTS OntologyVersion(id STRING PRIMARY KEY, version STRING, status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS IS_A(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS PART_OF(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS HAS_MEMBER(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS PART_OF_GEOGRAPHY(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS CONTAINS_GEOGRAPHY(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS HAS_CLASSIFICATION(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS HAS_PRIMARY_INDUSTRY(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS OPERATES_IN(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS DOMICILED_IN(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS HAS_FACILITY(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS HAS_EXPOSURE(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS AGAINST(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS MEASURED_BY(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS DENOMINATED_IN(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS AS_OF(FROM Concept TO Concept, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS ASSERTS(FROM Concept TO RelationshipAssertion)""",
"""CREATE REL TABLE IF NOT EXISTS TARGETS_ASSERTION(FROM RelationshipAssertion TO Concept)""",
"""CREATE REL TABLE IF NOT EXISTS HAS_RELATIONSHIP_TYPE(FROM RelationshipAssertion TO RelationshipType)""",
"""CREATE REL TABLE IF NOT EXISTS HAS_ROLE(FROM Concept TO SemanticRole)""",
"""CREATE REL TABLE IF NOT EXISTS HAS_SYNONYM(FROM Concept TO Synonym)""",
"""CREATE REL TABLE IF NOT EXISTS HAS_EXTERNAL_MAPPING(FROM Concept TO ExternalMapping)""",
"""CREATE REL TABLE IF NOT EXISTS HAS_VERSION(FROM Concept TO OntologyVersion)""",
]

SEMANTIC_DDL = [
"""CREATE NODE TABLE IF NOT EXISTS SemanticDataElement(id STRING PRIMARY KEY, name STRING, concept_id STRING, logical_dataset_id STRING, semantic_type STRING, definition STRING, expression STRING, aggregation STRING, grain STRING, status STRING, version STRING)""",
"""CREATE NODE TABLE IF NOT EXISTS LogicalDataset(id STRING PRIMARY KEY, name STRING, grain STRING, description STRING, status STRING, version STRING)""",
"""CREATE REL TABLE IF NOT EXISTS ELEMENT_PART_OF_DATASET(FROM SemanticDataElement TO LogicalDataset, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
]

METADATA_DDL = [
"""CREATE NODE TABLE IF NOT EXISTS PhysicalDataAsset(id STRING PRIMARY KEY, name STRING, database_name STRING, schema_name STRING, object_type STRING)""",
"""CREATE NODE TABLE IF NOT EXISTS PhysicalColumn(id STRING PRIMARY KEY, asset_id STRING, name STRING, data_type STRING, nullable BOOLEAN, is_key BOOLEAN)""",
"""CREATE REL TABLE IF NOT EXISTS ASSET_HAS_COLUMN(FROM PhysicalDataAsset TO PhysicalColumn, relationship_id STRING, confidence DOUBLE, approval_status STRING)""",
"""CREATE REL TABLE IF NOT EXISTS ASSET_JOINS_TO_ASSET(FROM PhysicalDataAsset TO PhysicalDataAsset, relationship_id STRING, source_column_id STRING, target_column_id STRING, cardinality STRING, preferred BOOLEAN, certified BOOLEAN, join_type STRING)""",
]

# Backwards-compatible aggregate name for callers that import DDL. It is intentionally
# not used to initialize a single database in the federated runtime.
DDL = ONTOLOGY_DDL + SEMANTIC_DDL + METADATA_DDL

def initialize(database_path: str, layer: str = "all"):
    layers = {"ontology": ONTOLOGY_DDL, "semantic": SEMANTIC_DDL, "metadata": METADATA_DDL, "all": DDL}
    repo = KuzuConnection(database_path)
    for statement in layers[layer]:
        repo.execute(statement)
    return repo

def initialize_federated(root_path: str):
    root = __import__('pathlib').Path(root_path)
    root.mkdir(parents=True, exist_ok=True)
    return {
        "ontology": initialize(str(root / "ontology"), "ontology"),
        "semantic": initialize(str(root / "semantic"), "semantic"),
        "metadata": initialize(str(root / "metadata"), "metadata"),
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="./data/kuzu/brso")
    parser.add_argument("--layer", choices=["all", "ontology", "semantic", "metadata"], default="all")
    args = parser.parse_args()
    initialize(args.db, args.layer)
    print(f"Initialized Kùzu schema at {args.db} ({args.layer})")
