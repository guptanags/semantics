from pydantic import BaseModel, Field
from typing import Any

class ScenarioQueryRequest(BaseModel):
    scenario_id: str
    vulnerability_id: str | None = None
    extraction_criteria: list[str] = Field(default_factory=list)
    scenario_context: dict[str, Any] = Field(default_factory=dict)
    dry_run: bool = True

class BusinessQueryRequest(BaseModel):
    query: str
    context: dict[str, Any] = Field(default_factory=dict)
    dry_run: bool = True

class UserQueryRequest(BaseModel):
    query: str
    context: dict[str, Any] = Field(default_factory=dict)
    dry_run: bool = True

class GraphRequest(BaseModel):
    layer: str = "all"
    limit: int = Field(default=250, ge=1, le=1000)
