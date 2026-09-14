from pydantic import BaseModel, Field
from typing import Optional

class OntologyConcept(BaseModel):
    id: str
    name: str
    concept_type: str = "BusinessConcept"
    domain: Optional[str] = None
    parent_id: Optional[str] = None
    definition: Optional[str] = None
    status: str = "ACTIVE"
    version: str = "brso-v0.1"

class OntologyRelationship(BaseModel):
    relationship_id: str
    relationship_type_id: str
    relationship_type: str
    source_id: str
    target_id: str
    inverse_type: Optional[str] = None
    cardinality: Optional[str] = None
    transitive: bool = False
    temporal: bool = False
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    approval_status: str = "approved"
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    ontology_version: str = "brso-v0.1"
    source_system: Optional[str] = None
    source_reference: Optional[str] = None
