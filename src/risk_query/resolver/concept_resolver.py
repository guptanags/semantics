from risk_query.domain.query_plan import ResolvedConcept

class AmbiguousConcept(Exception):
    pass

class ConceptNotFound(Exception):
    pass

class ConceptResolver:
    def __init__(self, ontology_repo):
        self.repo = ontology_repo

    def resolve(self, text: str) -> ResolvedConcept:
        result = self.repo.find_concepts(text)
        rows = result.get_all() if hasattr(result, "get_all") else []
        if len(rows) == 0:
            raise ConceptNotFound(text)
        if len(rows) > 1:
            raise AmbiguousConcept(f"{text}: {len(rows)} candidates")
        row = rows[0]
        return ResolvedConcept(
            requested=text,
            concept_id=row[0],
            concept_name=row[1],
            confidence=1.0,
            resolution_path=["EXACT_CANONICAL"],
        )
