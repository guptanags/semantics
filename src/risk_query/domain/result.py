from pydantic import BaseModel, Field
from typing import Any, Optional

class Provenance(BaseModel):
    query_id: str
    ontology_version: str
    semantic_version: Optional[str] = None
    metadata_version: Optional[str] = None
    source_datasets: list[str] = Field(default_factory=list)
    as_of_date: Optional[str] = None

class QueryResult(BaseModel):
    status: str
    data: list[dict[str, Any]] = Field(default_factory=list)
    row_count: int = 0
    sql: Optional[str] = None
    business_explanation: Optional[str] = None
    warnings: list[str] = Field(default_factory=list)
    provenance: Optional[Provenance] = None
