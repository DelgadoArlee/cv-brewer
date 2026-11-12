# Generation Service Module Technical Specification

## 1. Purpose

Implements the application-level LLM operations. The module owns the `LLMService` class that verifies generation requests and delegates availability checking, model discovery, and structured generation to a configured `LLMAdapter`.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `_validate_generation_request()` | Function | Verifies a generation request provides a model, at least one prompt message, and a JSON Schema. | `request: StructuredGenerationRequest` – Generation request to verify. | `None`. Raises `ValueError` when the request is incomplete. |
| `LLMService` | Class | Coordinates application-level LLM operations through a configured adapter. | `adapter: LLMAdapter` – Adapter that carries out the operations. | `LLMService` instance. |
| `LLMService.check_availability()` | Method | Reports whether the configured LLM service is reachable. | None. | `bool` – Availability outcome from the adapter. |
| `LLMService.list_models()` | Method | Lists the models available on the configured LLM service. | None. | `list[ModelInfo]` – Available model records. |
| `LLMService.generate_structured()` | Method | Verifies a generation request and delegates structured generation. | `request: StructuredGenerationRequest` – Generation request. | `dict[str, Any]` – Structured response from the adapter. Raises `ValueError` when the request is incomplete. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `LLMAdapter` | Internal interface | Carries out the delegated operations. See [Generation Adapter Module](adapter.md). |
| `ModelInfo`, `StructuredGenerationRequest` | Internal records | Data handled by the operations. See [Generation Models Module](models.md). |

## 4. Architecture Decision Log (ADL)

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/11/2026 | Established the service operations and required complete generation requests before delegation. | `_validate_generation_request()`, `LLMService`, `check_availability()`, `list_models()`, `generate_structured()` (added) | [Use an LLM Service abstraction with pluggable LLM adapters](../../../../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md) |

## 5. References

- [LLM Service Technical System Specification](../../../systems/llm-service/overview.md)
- [Generation Models Module](models.md)
- [Generation Adapter Module](adapter.md)
- [LLM Component Technical Specification](../../../technical-specification.md)
