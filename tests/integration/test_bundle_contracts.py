from pathlib import Path
from risk_query.okf.loader import OkfLoader

def test_semantic_bundle_loads():
    root=Path(__file__).parents[2]
    docs, _=OkfLoader().load(root/'knowledge/semantic')
    assert any(d['frontmatter']['kind']=='semantic_data_element' for d in docs)
    assert any(d['frontmatter']['kind']=='logical_dataset' for d in docs)

def test_metadata_bundle_loads():
    root=Path(__file__).parents[2]
    docs, _=OkfLoader().load(root/'knowledge/metadata')
    assert any(d['frontmatter']['kind']=='physical_data_asset' for d in docs)
    assert any(d['frontmatter']['kind']=='physical_column' for d in docs)
    assert any(d['frontmatter']['kind']=='physical_join' for d in docs)
