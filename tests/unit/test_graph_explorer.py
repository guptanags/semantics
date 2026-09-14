from risk_query.graph.repositories.graph_explorer_repo import GraphExplorerRepository

class FakeResult:
    def __init__(self, rows): self.rows = rows
    def get_all(self): return self.rows

class FakeGraph:
    def execute(self, query, parameters=None):
        if "MATCH (n:Concept)" in query:
            return FakeResult([[{"id":"brso.foundation.party","name":"Party","concept_type":"Entity"}]])
        if "MATCH (n:SemanticDataElement)" in query:
            return FakeResult([[{"id":"brso.semantic.party_id","name":"Party ID"}]])
        if "MATCH (n:LogicalDataset)" in query:
            return FakeResult([[{"id":"brso.dataset.party_exposure","name":"Party Exposure"}]])
        if "MATCH (n:PhysicalDataAsset)" in query:
            return FakeResult([[{"id":"brso.asset.dim_party","name":"DIM_PARTY"}]])
        if "MATCH (n:PhysicalColumn)" in query:
            return FakeResult([[{"id":"brso.column.dim_party.party_id","name":"PARTY_ID"}]])
        return FakeResult([])

def test_snapshot_returns_nodes():
    result = GraphExplorerRepository({"ontology":FakeGraph(), "semantic":FakeGraph(), "metadata":FakeGraph()}).snapshot("all", 20)
    assert result["layer"] == "all"
    assert any(n["id"] == "brso.foundation.party" for n in result["nodes"])
