from typing import Any

from core.services.llm.models import (
    ModelInfo,
    StructuredGenerationRequest,
)
from core.services.llm.port import LLMPort


def _validate_generation_request(request: StructuredGenerationRequest) -> None:
    if not request.model:
        raise ValueError("Generation request must identify a model.")
    if not request.messages:
        raise ValueError("Generation request must provide at least one prompt message.")
    if not request.json_schema:
        raise ValueError("Generation request must include a JSON Schema.")


class LLMService:
    def __init__(self, port: LLMPort) -> None:
        self._port = port

    def check_availability(self) -> bool:
        return self._port.check_availability()

    def list_models(self) -> list[ModelInfo]:
        return self._port.list_models()

    def generate_structured(self, request: StructuredGenerationRequest) -> dict[str, Any]:
        _validate_generation_request(request)
        return self._port.generate_structured(request).content
