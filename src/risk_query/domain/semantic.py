from pydantic import BaseModel, Field
from typing import Optional

class SemanticDataElement(BaseModel):
    id: str
    name: str
    concept_id: str
    logical_dataset_id: str
    semantic_type: Optional[str] = None
    definition: Optional[str] = None
    expression: Optional[str] = None
    aggregation: Optional[str] = None
    grain: Optional[str] = None
    status: str = "ACTIVE"
    version: str = "v1"

class LogicalDataset(BaseModel):
    id: str
    name: str
    grain: Optional[str] = None
    description: Optional[str] = None
    physical_asset_id: Optional[str] = None
    status: str = "ACTIVE"
    version: str = "v1"
