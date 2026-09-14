class SemanticRepository:
    def __init__(self, graph): self.graph=graph

    def elements_for_concept(self, concept_id: str):
        return self.graph.execute("""
          MATCH (e:SemanticDataElement)
          WHERE e.concept_id=$id AND e.status='ACTIVE'
          RETURN e
        """, {'id':concept_id})

    def dataset_for_element(self, element_id: str):
        return self.graph.execute("""
          MATCH (e:SemanticDataElement {id:$id})-[r:ELEMENT_PART_OF_DATASET]->(d:LogicalDataset)
          WHERE r.approval_status='approved'
          RETURN d
        """, {'id':element_id})
