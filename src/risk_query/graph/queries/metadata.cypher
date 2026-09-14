MATCH (d:LogicalDataset {id: $dataset_id})-[:IMPLEMENTED_BY]->(a:PhysicalDataAsset)
RETURN a

MATCH (a:PhysicalDataAsset {id: $asset_id})-[:ASSET_HAS_COLUMN]->(c:PhysicalColumn)
RETURN c
