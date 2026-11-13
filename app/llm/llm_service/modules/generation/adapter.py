from abc import ABC, abstractmethod
from typing import Any

from llm.llm_service.modules.generation.models import (
    ModelInfo,
    StructuredGenerationRequest,
)


class LLMAdapter(ABC):
    @abstractmethod
    def check_availability(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_models(self) -> list[ModelInfo]:
        raise NotImplementedError

    @abstractmethod
    def generate_structured(self, request: StructuredGenerationRequest) -> dict[str, Any]:
        raise NotImplementedError
