from hashlib import sha256

def rid(kind, source, target):
    return f"brso.graph.{kind}." + sha256(f"{source}|{target}".encode()).hexdigest()[:20]

class SemanticGraphIngester:
    """Ingest only semantic meaning. Cross-graph IDs are references, never graph edges."""
    def __init__(self, graph): self.graph = graph

    def ingest(self, documents):
        ids = {d["frontmatter"]["id"] for d in documents}
        for d in documents:
            fm = d["frontmatter"]
            kind = fm.get("kind")
            if kind == "logical_dataset":
                self._dataset(fm)
            elif kind == "semantic_data_element":
                self._element(fm, ids)
            else:
                raise ValueError(f"Unsupported semantic OKF kind: {kind}")
        for d in documents:
            fm = d["frontmatter"]
            if fm.get("kind") == "semantic_data_element":
                self._link_element_to_dataset(fm)

    def _dataset(self, fm):
        self.graph.execute("""
            MERGE (d:LogicalDataset {id: $id})
            SET d.name=$name, d.grain=$grain, d.description=$description,
                d.status=$status, d.version=$version
        """, {"id":fm["id"],"name":fm["title"],"grain":fm.get("grain"),
              "description":fm.get("description"),"status":fm["status"],"version":fm["version"]})

    def _element(self, fm, ids):
        if fm.get("logical_dataset_id") and fm["logical_dataset_id"] not in ids:
            raise ValueError(f"Unknown semantic logical_dataset_id={fm['logical_dataset_id']}")
        # concept_id intentionally remains an external ontology reference.
        self.graph.execute("""
            MERGE (e:SemanticDataElement {id: $id})
            SET e.name=$name, e.concept_id=$concept_id, e.logical_dataset_id=$logical_dataset_id,
                e.semantic_type=$semantic_type, e.definition=$definition, e.expression=$expression,
                e.aggregation=$aggregation, e.grain=$grain, e.status=$status, e.version=$version
        """, {"id":fm["id"],"name":fm["title"],"concept_id":fm.get("concept_id"),
              "logical_dataset_id":fm.get("logical_dataset_id"),"semantic_type":fm.get("semantic_type"),
              "definition":fm.get("description"),"expression":fm.get("expression"),
              "aggregation":fm.get("aggregation"),"grain":fm.get("grain"),
              "status":fm["status"],"version":fm["version"]})

    def _link_element_to_dataset(self, fm):
        element, dataset = fm["id"], fm["logical_dataset_id"]
        self.graph.execute("""
            MATCH (e:SemanticDataElement {id:$element})
            MATCH (d:LogicalDataset {id:$dataset})
            MERGE (e)-[:ELEMENT_PART_OF_DATASET {relationship_id:$rid, confidence:1.0, approval_status:'approved'}]->(d)
        """, {"element":element,"dataset":dataset,
              "rid":rid("element_dataset",element,dataset)})
