from core.services.logger import PerformanceMeasurement
from core.services.llm import (
    GenerationResult,
    LLMPort,
    LLMService,
    ModelInfo,
    StructuredGenerationRequest,
)
from core.services.llm.logger import LLMLogger


def _log_generation(
    logger: LLMLogger,
    request: StructuredGenerationRequest,
    performance: PerformanceMeasurement,
    result: GenerationResult | None,
    error: Exception | None,
) -> None:
    try:
        logger.record_generation(
            request,
            performance.finish(),
            result=result,
            error=error,
        )
    except Exception:
        return


class LoggingLLMPort(LLMPort):
    def __init__(self, wrapped: LLMPort, logger: LLMLogger) -> None:
        self._wrapped = wrapped
        self._logger = logger

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
            _log_generation(self._logger, request, performance, None, exc)
            raise
        _log_generation(self._logger, request, performance, result, None)
        return result
