from typing import Any

from llm.llm_service.modules.generation.adapter import LLMAdapter
from llm.llm_service.modules.generation.models import (
    ModelInfo,
    StructuredGenerationRequest,
)


def _validate_generation_request(request: StructuredGenerationRequest) -> None:
    if not request.model:
        raise ValueError("Generation request must identify a model.")
    if not request.messages:
        raise ValueError("Generation request must provide at least one prompt message.")
    if not request.json_schema:
        raise ValueError("Generation request must include a JSON Schema.")


class LLMService:
    def __init__(self, adapter: LLMAdapter) -> None:
        self._adapter = adapter

    def check_availability(self) -> bool:
        return self._adapter.check_availability()

    def list_models(self) -> list[ModelInfo]:
        return self._adapter.list_models()

    def generate_structured(self, request: StructuredGenerationRequest) -> dict[str, Any]:
        _validate_generation_request(request)
        return self._adapter.generate_structured(request)
