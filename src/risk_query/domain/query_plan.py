from pydantic import BaseModel, Field
from typing import Optional

class ResolvedConcept(BaseModel):
    requested: str
    concept_id: str
    concept_name: str
    confidence: float
    resolution_path: list[str] = Field(default_factory=list)

class ResolvedFilter(BaseModel):
    concept: ResolvedConcept
    operator: str
    value_ids: list[str] = Field(default_factory=list)
    value_text: str

class ResolvedMeasure(BaseModel):
    concept: ResolvedConcept
    aggregation: str
    semantic_element_id: Optional[str] = None

class QueryPlan(BaseModel):
    subject: ResolvedConcept
    filters: list[ResolvedFilter] = Field(default_factory=list)
    measures: list[ResolvedMeasure] = Field(default_factory=list)
    attributes: list[ResolvedConcept] = Field(default_factory=list)
    root_dataset_id: Optional[str] = None
    dataset_ids: list[str] = Field(default_factory=list)
    join_paths: list[dict] = Field(default_factory=list)
    grain: Optional[str] = None
    sql: Optional[str] = None
    resolution_status: str = "RESOLVED"
    warnings: list[str] = Field(default_factory=list)
