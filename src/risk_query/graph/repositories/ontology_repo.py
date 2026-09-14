class OntologyRepository:
    def __init__(self, graph):
        self.graph = graph

    def find_concepts(self, text: str):
        return self.graph.execute(
            """
            MATCH (c:Concept)
            WHERE lower(c.name) = lower($text)
               OR lower(c.id) = lower($text)
            RETURN c.id, c.name, c.concept_type, c.domain
            """,
            {"text": text},
        )

    def get_concept(self, concept_id: str):
        return self.graph.execute(
            "MATCH (c:Concept {id: $id}) RETURN c",
            {"id": concept_id},
        )

    def relationship_exists(self, rel_type: str, source_id: str, target_id: str):
        return self.graph.execute(
            f"""
            MATCH (s:Concept {{id: $source}})-[r:{rel_type}]->(t:Concept {{id: $target}})
            WHERE r.approval_status = 'approved'
            RETURN count(*) AS n
            """,
            {"source": source_id, "target": target_id},
        )
