import logging

from core.services.logger import PerformanceMeasurement
from core.services.llm import (
    GenerationResult,
    LLMPort,
    ModelInfo,
    StructuredGenerationRequest,
)
from core.services.llm.logger import LLMLogger

_LOGGER = logging.getLogger(__name__)


class LoggingLLMPort(LLMPort):
    def __init__(self, wrapped: LLMPort, logger: LLMLogger) -> None:
        self._wrapped = wrapped
        self._logger = logger
        self._processing_step_id: str | None = None

    @property
    def processing_step_id(self) -> str | None:
        return self._processing_step_id

    @processing_step_id.setter
    def processing_step_id(self, value: str | None) -> None:
        self._processing_step_id = value

    def set_processing_step_id(self, step_id: str | None) -> None:
        self._processing_step_id = step_id

    def _log_generation(
        self,
        request: StructuredGenerationRequest,
        performance: PerformanceMeasurement,
        result: GenerationResult | None,
        error: Exception | None,
    ) -> None:
        try:
            self._logger.record_generation(
                request,
                performance.finish(),
                result=result,
                error=error,
                processing_step_id=self._processing_step_id,
            )
        except Exception as exc:
            _LOGGER.error(
                "Failed to record structured generation activity log.",
                exc_info=exc,
            )

    def check_availability(self) -> bool:
        return self._wrapped.check_availability()

    def list_models(self) -> list[ModelInfo]:
        return self._wrapped.list_models()

    def generate_structured(
        self,
        request: StructuredGenerationRequest,
    ) -> GenerationResult:
        performance = PerformanceMeasurement.start()
        try:
            result = self._wrapped.generate_structured(request)
        except Exception as exc:
            self._log_generation(request, performance, None, exc)
            raise
        self._log_generation(request, performance, result, None)
        return result
