from abc import ABC, abstractmethod

from core.services.llm.models import GenerationResult, ModelInfo, StructuredGenerationRequest


class LLMPort(ABC):
    @abstractmethod
    def check_availability(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_models(self) -> list[ModelInfo]:
        raise NotImplementedError

    @abstractmethod
    def generate_structured(
        self,
        request: StructuredGenerationRequest,
    ) -> GenerationResult:
        raise NotImplementedError
