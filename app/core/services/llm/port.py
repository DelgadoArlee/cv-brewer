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

    def set_processing_step_id(self, step_id: str | None) -> None:
        return None
