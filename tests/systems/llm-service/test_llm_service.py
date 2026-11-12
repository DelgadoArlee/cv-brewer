from typing import Any

import pytest

from llm.adapters.ollama import LLMAdapterResponseError
from llm.llm_service import (
    ChatMessage,
    LLMAdapter,
    LLMService,
    ModelInfo,
    StructuredGenerationRequest,
)


class _FakeAdapter(LLMAdapter):
    def __init__(self) -> None:
        self.requests: list[StructuredGenerationRequest] = []
        self.available: bool = True
        self.models: list[ModelInfo] = []
        self.response: dict[str, Any] = {}
        self.failure: Exception | None = None

    def check_availability(self) -> bool:
        return self.available

    def list_models(self) -> list[ModelInfo]:
        if self.failure is not None:
            raise self.failure
        return self.models

    def generate_structured(self, request: StructuredGenerationRequest) -> dict[str, Any]:
        if self.failure is not None:
            raise self.failure
        self.requests.append(request)
        return self.response


def _complete_request() -> StructuredGenerationRequest:
    return StructuredGenerationRequest(
        model="llama3.1",
        messages=[ChatMessage(role="user", content="Parse this resume.")],
        json_schema={"type": "object"},
    )


def test_check_availability_returns_adapter_outcome() -> None:
    adapter = _FakeAdapter()

    adapter.available = True
    assert LLMService(adapter).check_availability() is True

    adapter.available = False
    assert LLMService(adapter).check_availability() is False


def test_list_models_returns_adapter_listing() -> None:
    adapter = _FakeAdapter()
    adapter.models = [ModelInfo(name="llama3.1:latest"), ModelInfo(name="qwen2.5:latest")]

    models = LLMService(adapter).list_models()

    assert models == adapter.models


def test_list_models_returns_empty_listing() -> None:
    adapter = _FakeAdapter()
    adapter.models = []

    assert LLMService(adapter).list_models() == []


def test_generate_structured_delegates_complete_request() -> None:
    adapter = _FakeAdapter()
    adapter.response = {"name": "Ada Lovelace"}
    request = _complete_request()

    response = LLMService(adapter).generate_structured(request)

    assert adapter.requests == [request]
    assert response == {"name": "Ada Lovelace"}


def test_generate_structured_rejects_request_without_model() -> None:
    adapter = _FakeAdapter()
    request = StructuredGenerationRequest(
        model="",
        messages=[ChatMessage(role="user", content="Parse this resume.")],
        json_schema={"type": "object"},
    )

    with pytest.raises(ValueError, match="model"):
        LLMService(adapter).generate_structured(request)

    assert adapter.requests == []


def test_generate_structured_rejects_request_without_messages() -> None:
    adapter = _FakeAdapter()
    request = StructuredGenerationRequest(
        model="llama3.1",
        messages=[],
        json_schema={"type": "object"},
    )

    with pytest.raises(ValueError, match="prompt message"):
        LLMService(adapter).generate_structured(request)

    assert adapter.requests == []


def test_generate_structured_rejects_request_without_schema() -> None:
    adapter = _FakeAdapter()
    request = StructuredGenerationRequest(
        model="llama3.1",
        messages=[ChatMessage(role="user", content="Parse this resume.")],
        json_schema={},
    )

    with pytest.raises(ValueError, match="JSON Schema"):
        LLMService(adapter).generate_structured(request)

    assert adapter.requests == []


def test_generate_structured_reports_adapter_failures() -> None:
    adapter = _FakeAdapter()
    adapter.failure = LLMAdapterResponseError("Ollama generation failed.")

    with pytest.raises(LLMAdapterResponseError):
        LLMService(adapter).generate_structured(_complete_request())

    assert adapter.requests == []
