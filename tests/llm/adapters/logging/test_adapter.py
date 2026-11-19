from typing import Any

import pytest
from core.services.logger import LogPerformance
from core.services.llm import (
    ChatMessage,
    GenerationResult,
    LLMPort,
    ModelInfo,
    StructuredGenerationRequest,
)
from core.services.llm.logger import LLMLogger
from llm.adapters.logging import LoggingLLMPort


class _FakePort(LLMPort):
    def __init__(self) -> None:
        self.result = GenerationResult(
            content={"name": "Ada"},
            response_content='{"name": "Ada"}',
        )
        self.failure: Exception | None = None
        self.requests: list[StructuredGenerationRequest] = []

    def check_availability(self) -> bool:
        return True

    def list_models(self) -> list[ModelInfo]:
        return [ModelInfo(name="llama3.1")]

    def generate_structured(
        self,
        request: StructuredGenerationRequest,
    ) -> GenerationResult:
        if self.failure is not None:
            raise self.failure
        self.requests.append(request)
        return self.result


class _FakeLogger(LLMLogger):
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def record_generation(self, request, performance, result=None, error=None):
        self.calls.append(
            {
                "request": request,
                "performance": performance,
                "result": result,
                "error": error,
            }
        )


def _request() -> StructuredGenerationRequest:
    return StructuredGenerationRequest(
        model="llama3.1",
        messages=[ChatMessage(role="user", content="Resume text.")],
        json_schema={"type": "object"},
    )


def test_generate_structured_returns_result_and_logs_success() -> None:
    port = _FakePort()
    logger = _FakeLogger()
    wrapper = LoggingLLMPort(port, logger)
    request = _request()

    result = wrapper.generate_structured(request)

    assert result is port.result
    assert port.requests == [request]
    assert len(logger.calls) == 1
    assert logger.calls[0]["result"] is port.result
    assert logger.calls[0]["error"] is None
    assert isinstance(logger.calls[0]["performance"], LogPerformance)


def test_generate_structured_reraises_and_logs_failure() -> None:
    port = _FakePort()
    port.failure = RuntimeError("failed")
    logger = _FakeLogger()
    wrapper = LoggingLLMPort(port, logger)

    with pytest.raises(RuntimeError, match="failed"):
        wrapper.generate_structured(_request())

    assert len(logger.calls) == 1
    assert isinstance(logger.calls[0]["error"], RuntimeError)
    assert logger.calls[0]["result"] is None


def test_non_generation_operations_are_delegated_without_logging() -> None:
    logger = _FakeLogger()
    wrapper = LoggingLLMPort(_FakePort(), logger)

    assert wrapper.check_availability() is True
    assert wrapper.list_models() == [ModelInfo(name="llama3.1")]
    assert logger.calls == []
