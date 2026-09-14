from risk_query.okf.loader import OkfLoader
from risk_query.okf.semantic_ingester import SemanticGraphIngester
from risk_query.okf.metadata_ingester import MetadataGraphIngester
from risk_query.okf.ontology_ingester import OntologyGraphIngester

class OkfGraphIngestionPipeline:
    """Ingest three physically disjoint Kùzu graphs plus an external federation registry."""
    def __init__(self, ontology_graph, semantic_graph, metadata_graph, federation=None):
        self.ontology_graph = ontology_graph
        self.semantic_graph = semantic_graph
        self.metadata_graph = metadata_graph
        self.federation = federation
        self.loader = OkfLoader()

    def ingest(self, ontology_dir: str, semantic_dir: str, metadata_dir: str):
        ontology_docs, _ = self.loader.load(ontology_dir)
        semantic_docs, _ = self.loader.load(semantic_dir)
        metadata_docs, _ = self.loader.load(metadata_dir)
        self._validate_semantic(semantic_docs)
        self._validate_metadata(metadata_docs)
        OntologyGraphIngester(self.ontology_graph).ingest(ontology_docs)
        MetadataGraphIngester(self.metadata_graph).ingest(metadata_docs)
        SemanticGraphIngester(self.semantic_graph).ingest(semantic_docs)
        return {
            'ontology_documents': len(ontology_docs),
            'semantic_documents': len(semantic_docs),
            'metadata_documents': len(metadata_docs),
            'status': 'INGESTED',
            'federation_registry': bool(self.federation),
        }

    def _validate_semantic(self, docs):
        ids={d['frontmatter']['id'] for d in docs}
        for d in docs:
            fm=d['frontmatter']
            if fm.get('kind') == 'semantic_data_element' and fm.get('logical_dataset_id') not in ids:
                raise ValueError(f"Unresolved semantic dataset: {fm.get('logical_dataset_id')}")

    def _validate_metadata(self, docs):
        ids={d['frontmatter']['id'] for d in docs}
        for d in docs:
            fm=d['frontmatter']
            if fm.get('kind') == 'physical_column' and fm.get('asset_id') not in ids:
                raise ValueError(f"Unresolved asset: {fm.get('asset_id')}")
            if fm.get('kind') == 'physical_join':
                for field in ('source_asset_id','target_asset_id','source_column_id','target_column_id'):
                    if fm.get(field) not in ids:
                        raise ValueError(f"Unresolved metadata reference: {field}={fm.get(field)}")
