from pathlib import Path

def test_schema_has_no_cross_graph_edges():
    text=(Path(__file__).parents[2]/'src/risk_query/graph/schema.py').read_text()
    assert 'FROM Concept TO SemanticDataElement' not in text
    assert 'FROM LogicalDataset TO PhysicalDataAsset' not in text
    assert 'FROM SemanticDataElement TO PhysicalColumn' not in text

def test_semantic_okf_contains_no_physical_binding_fields():
    root=Path(__file__).parents[2]
    for path in (root/'knowledge/semantic').glob('*.okf.md'):
        text=path.read_text()
        assert 'physical_column_id:' not in text
        assert 'physical_asset_id:' not in text
