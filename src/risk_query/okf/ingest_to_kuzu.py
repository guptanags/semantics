from hashlib import sha256
from datetime import datetime, timezone

ALLOWED_RELATIONSHIPS = {
    "IS_A", "PART_OF", "HAS_PRIMARY_INDUSTRY", "OPERATES_IN",
    "DOMICILED_IN", "HAS_FACILITY", "HAS_EXPOSURE", "AGAINST",
    "MEASURED_BY", "DENOMINATED_IN", "AS_OF",
}

RELATIONSHIP_TYPE_IDS = {
    name: f"brso.rel.{name.lower()}" for name in ALLOWED_RELATIONSHIPS
}

def assertion_id(source, rel, target):
    return "brso.assertion." + sha256(
        f"{source}|{rel}|{target}".encode()
    ).hexdigest()[:24]

class KuzuOkfIngester:
    """Loads curated OKF ontology bundles into the ontology graph.

    This service deliberately uses a two-stage process:
      1. validate/parse the complete bundle;
      2. create nodes and approved typed edges.

    RelationshipType nodes are created before assertions so the graph is
    internally referentially complete.
    """

    def __init__(self, graph):
        self.graph = graph

    def _merge_concept(self, fm, body):
        self.graph.execute(
            """
            MERGE (c:Concept {id: $id})
            SET c.name = $name,
                c.concept_type = $concept_type,
                c.domain = $domain,
                c.definition = $definition,
                c.status = $status,
                c.version = $version
            """,
            {
                "id": fm["id"],
                "name": fm["title"],
                "concept_type": fm.get("concept_type", "BusinessConcept"),
                "domain": fm.get("domain"),
                "definition": fm.get("description", body[:1000]),
                "status": fm["status"],
                "version": fm["version"],
            },
        )

    def _merge_relationship_type(self, rel_type):
        self.graph.execute(
            """
            MERGE (r:RelationshipType {id: $id})
            SET r.name = $name,
                r.inverse_type = $inverse,
                r.domain_concept_type = $domain,
                r.range_concept_type = $range,
                r.transitive = $transitive,
                r.symmetric = $symmetric,
                r.temporal = $temporal,
                r.resolution_priority = $priority,
                r.status = $status,
                r.version = $version
            """,
            {
                "id": rel_type["id"],
                "name": rel_type["name"],
                "inverse": rel_type.get("inverse_type"),
                "domain": rel_type.get("domain_concept_type"),
                "range": rel_type.get("range_concept_type"),
                "transitive": bool(rel_type.get("transitive", False)),
                "symmetric": bool(rel_type.get("symmetric", False)),
                "temporal": bool(rel_type.get("temporal", False)),
                "priority": int(rel_type.get("resolution_priority", 100)),
                "status": rel_type.get("status", "ACTIVE"),
                "version": rel_type.get("version", "brso-v0.1"),
            },
        )

    def ingest(self, documents, relationships, relationship_registry):
        # 1. Concepts first.
        for doc in documents:
            self._merge_concept(doc["frontmatter"], doc["body"])

        # 2. Relationship types before assertions.
        for rel in relationship_registry:
            self._merge_relationship_type(rel)

        # 3. Typed relationships + reified assertions.
        for rel in relationships:
            name = rel["relationship_type"]
            if name not in ALLOWED_RELATIONSHIPS:
                raise ValueError(f"Relationship not in production allowlist: {name}")

            source = rel["source_id"]
            target = rel["target_id"]
            aid = assertion_id(source, name, target)
            now = datetime.now(timezone.utc).isoformat()

            self.graph.execute(
                f"""
                MATCH (s:Concept {{id: $source}})
                MATCH (t:Concept {{id: $target}})
                MERGE (s)-[r:{name} {{relationship_id: $aid}}]->(t)
                SET r.confidence = $confidence,
                    r.approval_status = $approval,
                    r.relationship_id = $aid
                """,
                {
                    "source": source,
                    "target": target,
                    "aid": aid,
                    "confidence": rel["confidence"],
                    "approval": rel["approval_status"],
                },
            )

            self.graph.execute(
                """
                MERGE (a:RelationshipAssertion {id: $aid})
                SET a.relationship_type_id = $rtid,
                    a.source_id = $source,
                    a.target_id = $target,
                    a.valid_from = $valid_from,
                    a.valid_to = $valid_to,
                    a.asserted_at = $asserted_at,
                    a.confidence = $confidence,
                    a.approval_status = $approval,
                    a.source_reference = $source_reference,
                    a.ontology_version = $version
                """,
                {
                    "aid": aid,
                    "rtid": RELATIONSHIP_TYPE_IDS[name],
                    "source": source,
                    "target": target,
                    "valid_from": rel.get("valid_from"),
                    "valid_to": rel.get("valid_to"),
                    "asserted_at": now,
                    "confidence": rel["confidence"],
                    "approval": rel["approval_status"],
                    "source_reference": rel.get("source_reference"),
                    "version": "brso-v0.1",
                },
            )

            self.graph.execute(
                """
                MATCH (s:Concept {id: $source})
                MATCH (a:RelationshipAssertion {id: $aid})
                MATCH (t:Concept {id: $target})
                MATCH (rt:RelationshipType {id: $rtid})
                MERGE (s)-[:ASSERTS]->(a)
                MERGE (a)-[:TARGETS_ASSERTION]->(t)
                MERGE (a)-[:HAS_RELATIONSHIP_TYPE]->(rt)
                """,
                {
                    "source": source,
                    "target": target,
                    "aid": aid,
                    "rtid": RELATIONSHIP_TYPE_IDS[name],
                },
            )
