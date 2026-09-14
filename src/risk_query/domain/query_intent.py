from pydantic import BaseModel, Field
from typing import Literal, Any

class FilterValue(BaseModel):
    text: str
    semantic_type: str | None = None
    resolved_ids: list[str] = Field(default_factory=list)

class QueryFilter(BaseModel):
    concept: str
    operator: Literal["EQ", "IN", "NOT_IN", "GT", "GTE", "LT", "LTE"]
    value: FilterValue

class QueryMeasure(BaseModel):
    concept: str
    aggregation: Literal["SUM", "AVG", "COUNT", "MIN", "MAX"]

class QueryIntent(BaseModel):
    subject: str
    filters: list[QueryFilter] = Field(default_factory=list)
    measures: list[QueryMeasure] = Field(default_factory=list)
    requested_attributes: list[str] = Field(default_factory=list)
    as_of_date: str | None = None
    limit: int | None = None
    context: dict[str, Any] = Field(default_factory=dict)
