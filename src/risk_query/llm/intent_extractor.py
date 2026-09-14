from pathlib import Path
from risk_query.domain.query_intent import QueryIntent

class IntentExtractor:
    def __init__(self, vertex_client, prompt_path: str):
        self.vertex = vertex_client
        self.prompt_template = Path(prompt_path).read_text()

    def extract(self, criteria: list[str], context: dict) -> QueryIntent:
        prompt = self.prompt_template.format(
            criteria="\n".join(f"- {x}" for x in criteria),
            context=context,
        )
        payload = self.vertex.generate_json(prompt)
        return QueryIntent.model_validate(payload)
