from __future__ import annotations
import json
from typing import Any

class VertexAIClient:
    """Thin boundary around Vertex AI. Keep provider-specific code here."""

    def __init__(self, project_id: str, location: str, model: str):
        self.project_id = project_id
        self.location = location
        self.model = model
        self._model = None

    def _ensure_model(self):
        if self._model is not None:
            return
        import vertexai
        from vertexai.generative_models import GenerativeModel
        vertexai.init(project=self.project_id, location=self.location)
        self._model = GenerativeModel(self.model)

    def generate_json(self, prompt: str) -> dict[str, Any]:
        self._ensure_model()
        response = self._model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"},
        )
        return json.loads(response.text)
