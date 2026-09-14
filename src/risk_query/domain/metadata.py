from pydantic import BaseModel
from typing import Optional

class PhysicalDataAsset(BaseModel):
    id: str
    name: str
    database: Optional[str] = None
    schema_name: Optional[str] = None
    object_type: str = "TABLE"
    description: Optional[str] = None

class PhysicalColumn(BaseModel):
    id: str
    asset_id: str
    name: str
    data_type: str
    nullable: bool = True
    is_key: bool = False

class JoinPath(BaseModel):
    source_asset_id: str
    target_asset_id: str
    source_column: str
    target_column: str
    cardinality: str = "MANY_TO_ONE"
    preferred: bool = False
    certified: bool = False
    relationship_name: Optional[str] = None
