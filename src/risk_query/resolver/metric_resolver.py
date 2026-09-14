class MetricResolver:
    def __init__(self, semantic_repo):
        self.semantic_repo = semantic_repo

    def resolve(self, concept_id: str):
        return self.semantic_repo.elements_for_concept(concept_id)
