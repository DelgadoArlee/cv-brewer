import json
from typing import Any

import httpx
from core.services.llm import (
    GenerationResult,
    GenerationUsage,
    LLMPort,
    ModelInfo,
    StructuredGenerationRequest,
)

from llm.adapters.ollama.config import OllamaConfig
from llm.adapters.ollama.errors import (
    LLMAdapterConnectionError,
    LLMAdapterModelNotFoundError,
    LLMAdapterResponseError,
    LLMAdapterTimeoutError,
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


def _extract_response_content(body: Any) -> str:
    if not isinstance(body, dict):
        raise LLMAdapterResponseError("Ollama generation response is malformed.")
    message = body.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise LLMAdapterResponseError("Ollama generation response is missing message content.")
    return message["content"]


def _extract_optional_int(body: dict[str, Any], key: str) -> int | None:
    value = body.get(key)
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    return None


def _extract_generation_usage(body: dict[str, Any]) -> GenerationUsage:
    input_tokens = _extract_optional_int(body, "prompt_eval_count")
    output_tokens = _extract_optional_int(body, "eval_count")
    total_tokens = (
        input_tokens + output_tokens
        if input_tokens is not None and output_tokens is not None
        else None
    )
    return GenerationUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    )


def _extract_finish_reason(body: dict[str, Any]) -> str | None:
    reason = body.get("done_reason")
    return reason if isinstance(reason, str) else None


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


class OllamaAdapter(LLMPort):
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

    def generate_structured(
        self,
        request: StructuredGenerationRequest,
    ) -> GenerationResult:
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
        if not isinstance(body, dict):
            raise LLMAdapterResponseError("Ollama generation response is malformed.")
        response_content = _extract_response_content(body)
        return GenerationResult(
            content=_parse_structured_content(response_content),
            response_content=response_content,
            finish_reason=_extract_finish_reason(body),
            usage=_extract_generation_usage(body),
        )
