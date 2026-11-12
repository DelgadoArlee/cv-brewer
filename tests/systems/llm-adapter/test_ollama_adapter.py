from collections.abc import Callable

import httpx
import pytest

import json

from llm.adapters.ollama import (
    LLMAdapterConnectionError,
    LLMAdapterModelNotFoundError,
    LLMAdapterResponseError,
    LLMAdapterTimeoutError,
    OllamaAdapter,
    OllamaConfig,
    create_ollama_client,
)
from llm.llm_service import ChatMessage, StructuredGenerationRequest

Handler = Callable[[httpx.Request], httpx.Response]


@pytest.fixture
def make_adapter():
    clients: list[httpx.Client] = []

    def _make(handler: Handler) -> OllamaAdapter:
        client = httpx.Client(
            transport=httpx.MockTransport(handler),
            base_url="http://ollama.test",
        )
        clients.append(client)
        return OllamaAdapter(client)

    yield _make

    for client in clients:
        client.close()


def _generation_request() -> StructuredGenerationRequest:
    return StructuredGenerationRequest(
        model="llama3.1",
        messages=[ChatMessage(role="user", content="Parse this resume.")],
        json_schema={"type": "object", "properties": {"name": {"type": "string"}}},
    )


def test_config_holds_default_values() -> None:
    config = OllamaConfig()

    assert config.base_url == "http://localhost:11434"
    assert config.connect_timeout_seconds == 5.0
    assert config.read_timeout_seconds == 300.0


def test_create_ollama_client_uses_configuration() -> None:
    config = OllamaConfig(
        base_url="http://ollama.test:11434",
        connect_timeout_seconds=2.0,
        read_timeout_seconds=60.0,
    )
    client = create_ollama_client(config)

    try:
        assert str(client.base_url).startswith("http://ollama.test:11434")
        assert client.timeout.connect == 2.0
        assert client.timeout.read == 60.0
    finally:
        client.close()


def test_check_availability_reports_available(make_adapter) -> None:
    adapter = make_adapter(lambda request: httpx.Response(200, json={"version": "0.6.9"}))

    assert adapter.check_availability() is True


def test_check_availability_reports_unreachable_service(make_adapter) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused")

    adapter = make_adapter(handler)

    assert adapter.check_availability() is False


def test_check_availability_reports_timeout(make_adapter) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out")

    adapter = make_adapter(handler)

    assert adapter.check_availability() is False


def test_check_availability_reports_failed_status(make_adapter) -> None:
    adapter = make_adapter(lambda request: httpx.Response(500))

    assert adapter.check_availability() is False


def test_list_models_returns_models(make_adapter) -> None:
    adapter = make_adapter(
        lambda request: httpx.Response(
            200,
            json={
                "models": [
                    {"name": "llama3.1:latest"},
                    {"name": "qwen2.5:latest"},
                ]
            },
        )
    )

    models = adapter.list_models()

    assert [model.name for model in models] == ["llama3.1:latest", "qwen2.5:latest"]


def test_list_models_returns_empty_listing(make_adapter) -> None:
    adapter = make_adapter(lambda request: httpx.Response(200, json={"models": []}))

    assert adapter.list_models() == []


def test_list_models_translates_connection_failures(make_adapter) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused")

    adapter = make_adapter(handler)

    with pytest.raises(LLMAdapterConnectionError):
        adapter.list_models()


def test_list_models_translates_timeouts(make_adapter) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out")

    adapter = make_adapter(handler)

    with pytest.raises(LLMAdapterTimeoutError):
        adapter.list_models()


def test_list_models_translates_failed_responses(make_adapter) -> None:
    adapter = make_adapter(lambda request: httpx.Response(500))

    with pytest.raises(LLMAdapterResponseError):
        adapter.list_models()


def test_list_models_translates_invalid_json(make_adapter) -> None:
    adapter = make_adapter(lambda request: httpx.Response(200, content="not json"))

    with pytest.raises(LLMAdapterResponseError):
        adapter.list_models()


def test_list_models_translates_malformed_payloads(make_adapter) -> None:
    adapter = make_adapter(lambda request: httpx.Response(200, json={"unexpected": True}))

    with pytest.raises(LLMAdapterResponseError):
        adapter.list_models()


def test_generate_structured_returns_parsed_json_object(make_adapter) -> None:
    adapter = make_adapter(
        lambda request: httpx.Response(
            200,
            json={
                "message": {"role": "assistant", "content": '{"name": "Ada Lovelace"}'},
                "done": True,
            },
        )
    )

    response = adapter.generate_structured(_generation_request())

    assert response == {"name": "Ada Lovelace"}


def test_generate_structured_sends_messages_and_schema_unchanged(make_adapter) -> None:
    captured: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(json.loads(request.content))
        return httpx.Response(
            200,
            json={
                "message": {"role": "assistant", "content": '{"name": "Ada Lovelace"}'},
                "done": True,
            },
        )

    adapter = make_adapter(handler)
    request = _generation_request()

    adapter.generate_structured(request)

    assert len(captured) == 1
    assert captured[0]["model"] == request.model
    assert captured[0]["messages"] == [{"role": "user", "content": "Parse this resume."}]
    assert captured[0]["stream"] is False
    assert captured[0]["format"] == request.json_schema


def test_generate_structured_translates_invalid_json_content(make_adapter) -> None:
    adapter = make_adapter(
        lambda request: httpx.Response(
            200,
            json={
                "message": {"role": "assistant", "content": "not json"},
                "done": True,
            },
        )
    )

    with pytest.raises(LLMAdapterResponseError):
        adapter.generate_structured(_generation_request())


def test_generate_structured_translates_non_object_content(make_adapter) -> None:
    adapter = make_adapter(
        lambda request: httpx.Response(
            200,
            json={
                "message": {"role": "assistant", "content": "[1, 2]"},
                "done": True,
            },
        )
    )

    with pytest.raises(LLMAdapterResponseError):
        adapter.generate_structured(_generation_request())


def test_generate_structured_translates_missing_model(make_adapter) -> None:
    adapter = make_adapter(
        lambda request: httpx.Response(404, json={"error": "model not found"})
    )

    with pytest.raises(LLMAdapterModelNotFoundError):
        adapter.generate_structured(_generation_request())


def test_generate_structured_translates_connection_failures(make_adapter) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused")

    adapter = make_adapter(handler)

    with pytest.raises(LLMAdapterConnectionError):
        adapter.generate_structured(_generation_request())


def test_generate_structured_translates_timeouts(make_adapter) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out")

    adapter = make_adapter(handler)

    with pytest.raises(LLMAdapterTimeoutError):
        adapter.generate_structured(_generation_request())


def test_generate_structured_translates_failed_responses(make_adapter) -> None:
    adapter = make_adapter(lambda request: httpx.Response(500))

    with pytest.raises(LLMAdapterResponseError):
        adapter.generate_structured(_generation_request())
