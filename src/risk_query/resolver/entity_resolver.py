class EntityResolver:
    def __init__(self, ontology_repo):
        self.repo = ontology_repo

    def resolve_value(self, value_text: str, semantic_type: str | None = None) -> list[str]:
        # Reference implementation: entity/value resolution should use
        # governed code lists and explicit identifiers, not LLM guessing.
        return []
