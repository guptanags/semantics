from pathlib import Path
from risk_query.okf.loader import OkfLoader

def test_all_okf_layers_have_closed_internal_references():
    root=Path(__file__).parents[2]
    for layer in ('ontology','semantic','metadata'):
        docs,_=OkfLoader().load(root/'knowledge'/layer)
        assert docs

def test_semantic_graph_has_no_physical_bindings():
    root=Path(__file__).parents[2]
    docs,_=OkfLoader().load(root/'knowledge/semantic')
    for d in docs:
        fm=d['frontmatter']
        if fm.get('kind') == 'semantic_data_element':
            assert fm.get('concept_id')
            assert fm.get('logical_dataset_id')
            assert not fm.get('physical_column_id')
        elif fm.get('kind') == 'logical_dataset':
            assert not fm.get('physical_asset_id')

def test_metadata_join_contract():
    root=Path(__file__).parents[2]
    docs,_=OkfLoader().load(root/'knowledge/metadata')
    joins=[d['frontmatter'] for d in docs if d['frontmatter'].get('kind')=='physical_join']
    assert joins
    assert all(j['cardinality'] in {'MANY_TO_ONE','ONE_TO_MANY','ONE_TO_ONE','MANY_TO_MANY'} for j in joins)
    assert all('source_column_id' in j and 'target_column_id' in j for j in joins)
