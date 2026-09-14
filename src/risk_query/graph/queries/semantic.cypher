MATCH (c:Concept {id: $concept_id})-[r:REPRESENTED_BY]->(e:SemanticDataElement)
WHERE r.approval_status = 'approved'
RETURN e
