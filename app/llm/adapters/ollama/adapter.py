import json
from typing import Any

import httpx

from llm.adapters.ollama.config import OllamaConfig
from llm.adapters.ollama.errors import (
    LLMAdapterConnectionError,
    LLMAdapterModelNotFoundError,
    LLMAdapterResponseError,
    LLMAdapterTimeoutError,
)
from llm.llm_service.modules.generation.models import (
    ModelInfo,
    StructuredGenerationRequest,
)


def create_ollama_client(config: OllamaConfig) -> httpx.Client:
    return httpx.Client(
        base_url=config.base_url,
        timeout=httpx.Timeout(
            connect=config.connect_timeout_seconds,
            read=config.read_timeout_seconds,
            write=config.connect_timeout_seconds,
            pool=config.connect_timeout_seconds,
        ),
    )


def _parse_model_listing(payload: Any) -> list[ModelInfo]:
    if not isinstance(payload, dict) or not isinstance(payload.get("models"), list):
        raise LLMAdapterResponseError("Ollama model listing response is malformed.")
    models = []
    for entry in payload["models"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            raise LLMAdapterResponseError("Ollama model listing entry is malformed.")
        models.append(ModelInfo(name=entry["name"]))
    return models


def _extract_message_content(body: Any) -> str:
    if not isinstance(body, dict):
        raise LLMAdapterResponseError("Ollama generation response is malformed.")
    message = body.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise LLMAdapterResponseError("Ollama generation response is missing message content.")
    return message["content"]


def _parse_structured_content(content: str) -> dict[str, Any]:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise LLMAdapterResponseError(
            "Ollama structured response content is not valid JSON."
        ) from exc
    if not isinstance(parsed, dict):
        raise LLMAdapterResponseError("Ollama structured response content is not a JSON object.")
    return parsed


class OllamaAdapter:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def check_availability(self) -> bool:
        try:
            response = self._client.get("/api/version")
        except httpx.TransportError:
            return False
        return response.status_code == 200

    def list_models(self) -> list[ModelInfo]:
        try:
            response = self._client.get("/api/tags")
        except httpx.TimeoutException as exc:
            raise LLMAdapterTimeoutError(
                "Ollama model listing request timed out."
            ) from exc
        except httpx.TransportError as exc:
            raise LLMAdapterConnectionError(
                "Ollama service could not be reached."
            ) from exc
        if response.status_code != 200:
            raise LLMAdapterResponseError(
                f"Ollama model listing failed with status {response.status_code}."
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise LLMAdapterResponseError(
                "Ollama model listing response is not valid JSON."
            ) from exc
        return _parse_model_listing(payload)

    def generate_structured(self, request: StructuredGenerationRequest) -> dict[str, Any]:
        payload = {
            "model": request.model,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in request.messages
            ],
            "stream": False,
            "format": request.json_schema,
        }
        try:
            response = self._client.post("/api/chat", json=payload)
        except httpx.TimeoutException as exc:
            raise LLMAdapterTimeoutError(
                f"Ollama generation request for model '{request.model}' timed out."
            ) from exc
        except httpx.TransportError as exc:
            raise LLMAdapterConnectionError(
                "Ollama service could not be reached."
            ) from exc
        if response.status_code == 404:
            raise LLMAdapterModelNotFoundError(
                f"Model '{request.model}' was not found on the Ollama service."
            )
        if response.status_code != 200:
            raise LLMAdapterResponseError(
                f"Ollama generation failed with status {response.status_code}."
            )
        try:
            body = response.json()
        except ValueError as exc:
            raise LLMAdapterResponseError(
                "Ollama generation response is not valid JSON."
            ) from exc
        content = _extract_message_content(body)
        return _parse_structured_content(content)
