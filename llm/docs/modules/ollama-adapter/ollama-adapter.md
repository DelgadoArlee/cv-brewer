# Ollama Adapter Module Technical Specification

## 1. Purpose

Provides the Ollama-specific implementation for the LLM component. The module owns Ollama configuration, the adapter-local error hierarchy, the synchronous `httpx` client factory, and the `OllamaAdapter` class that implements the `LLMAdapter` contract against the user's Ollama service.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `DEFAULT_OLLAMA_BASE_URL` | Constant | Default Ollama service endpoint: `http://localhost:11434`. | None. | None. |
| `OllamaConfig` | Dataclass | Holds the Ollama service base URL and request timeouts. | `base_url: str = DEFAULT_OLLAMA_BASE_URL` – Ollama service endpoint. `connect_timeout_seconds: float = 5.0` – Connection timeout. `read_timeout_seconds: float = 300.0` – Response read timeout for long generations. | `OllamaConfig` instance. |
| `LLMAdapterError` | Exception class | Base class for LLM adapter failures. | `message: str` – Error description. | `LLMAdapterError` instance. |
| `LLMAdapterConnectionError` | Exception class | Represents external LLM services that cannot be reached. | `message: str` – Error description. | `LLMAdapterConnectionError` instance. |
| `LLMAdapterTimeoutError` | Exception class | Represents requests that exceeded the configured timeout. | `message: str` – Error description. | `LLMAdapterTimeoutError` instance. |
| `LLMAdapterResponseError` | Exception class | Represents failed or invalid service responses. | `message: str` – Error description. | `LLMAdapterResponseError` instance. |
| `LLMAdapterModelNotFoundError` | Exception class | Represents models that are not available on the service. | `message: str` – Error description. | `LLMAdapterModelNotFoundError` instance. |
| `create_ollama_client()` | Function | Creates a synchronous `httpx` client bound to the configured base URL and timeouts. | `config: OllamaConfig` – Ollama configuration. | `httpx.Client`. |
| `_parse_model_listing()` | Function | Parses an Ollama model listing payload into model records. | `payload: Any` – Parsed service response body. | `list[ModelInfo]`. Raises `LLMAdapterResponseError` on malformed payloads. |
| `_extract_message_content()` | Function | Extracts the message content from an Ollama generation response body. | `body: Any` – Parsed service response body. | `str` – Message content. Raises `LLMAdapterResponseError` on malformed bodies. |
| `_parse_structured_content()` | Function | Parses generation response content into a JSON object. | `content: str` – Message content returned by the model. | `dict[str, Any]`. Raises `LLMAdapterResponseError` on invalid or non-object content. |
| `OllamaAdapter` | Class | Implements the `LLMAdapter` contract for the Ollama service. | `client: httpx.Client` – Client used for Ollama communication. The caller owns the client lifecycle. | `OllamaAdapter` instance. |
| `OllamaAdapter.check_availability()` | Method | Verifies the Ollama service is reachable through a lightweight version request. | None. | `bool` – `False` when communication fails. |
| `OllamaAdapter.list_models()` | Method | Lists models from the Ollama model listing endpoint. | None. | `list[ModelInfo]`. Raises adapter errors on failures. |
| `OllamaAdapter.generate_structured()` | Method | Sends prompt messages and the JSON Schema to the selected model through the chat endpoint with streaming disabled and the schema passed through the structured-output format field. | `request: StructuredGenerationRequest` – Generation request. | `dict[str, Any]`. Raises adapter errors on failures. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `httpx` | External library | Synchronous HTTP client for Ollama communication. |
| `LLMAdapter` | Internal interface | Defines the contract implemented by `OllamaAdapter`. See [Generation Adapter Module](../llm-service/generation/adapter.md). |
| `ModelInfo`, `StructuredGenerationRequest` | Internal records | Application-level data handled by the adapter. See [Generation Models Module](../llm-service/generation/models.md). |
| Python `json` | Standard library | Parses structured response content. |

## 4. Architecture Decision Log (ADL)

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/11/2026 | Established the Ollama adapter foundation with synchronous `httpx`, adapter-local configuration and errors, lightweight availability verification, model listing, and structured outputs through the chat endpoint. | `DEFAULT_OLLAMA_BASE_URL`, `OllamaConfig`, error classes, `create_ollama_client()`, `OllamaAdapter` and its methods, parsing helpers (added) | [Establish the Ollama adapter foundation](../../adr/11-11-26/ollama-adapter-foundation.md) |

## 5. References

- [LLM Adapter Technical System Specification](../../systems/llm-adapter/overview.md)
- [Generation Adapter Module](../llm-service/generation/adapter.md)
- [Generation Models Module](../llm-service/generation/models.md)
- [Ollama Adapter Foundation ADR](../../adr/11-11-26/ollama-adapter-foundation.md)
- [LLM Component Technical Specification](../../technical-specification.md)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [httpx Documentation](https://www.python-httpx.org/)
