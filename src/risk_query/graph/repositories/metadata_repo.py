class MetadataRepository:
    def __init__(self, graph): self.graph=graph

    def asset(self, asset_id: str):
        return self.graph.execute("MATCH (a:PhysicalDataAsset {id:$id}) RETURN a", {'id':asset_id})

    def columns_for_asset(self, asset_id: str):
        return self.graph.execute("""
          MATCH (a:PhysicalDataAsset {id:$id})-[:ASSET_HAS_COLUMN]->(c:PhysicalColumn)
          RETURN c
        """, {'id':asset_id})

    def join_paths(self, source_asset_id: str):
        return self.graph.execute("""
          MATCH (s:PhysicalDataAsset {id:$id})-[r:ASSET_JOINS_TO_ASSET]->(t:PhysicalDataAsset)
          WHERE r.certified=true
          RETURN t.id, r.source_column_id, r.target_column_id, r.cardinality,
                 r.preferred, r.certified, r.join_type
        """, {'id':source_asset_id})
