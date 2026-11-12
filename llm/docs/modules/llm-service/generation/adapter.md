# Generation Adapter Module Technical Specification

## 1. Purpose

Defines the adapter contract implemented by LLM Adapter implementations. The module owns the abstract `LLMAdapter` interface that carries out application-level LLM operations for a specific external LLM service.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `LLMAdapter` | Abstract class | Defines the adapter contract for a specific external LLM service. | None. | `LLMAdapter` subclass instances. |
| `LLMAdapter.check_availability()` | Abstract method | Verifies that the external LLM service is reachable. | None. | `bool` – Whether the service is available. |
| `LLMAdapter.list_models()` | Abstract method | Lists the models available on the external LLM service. | None. | `list[ModelInfo]` – Available model records. |
| `LLMAdapter.generate_structured()` | Abstract method | Generates a schema-constrained structured response. | `request: StructuredGenerationRequest` – Complete generation request. | `dict[str, Any]` – Generated structured response. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `ChatMessage`, `ModelInfo`, `StructuredGenerationRequest` | Internal records | Data handled by the adapter contract. See [Generation Models Module](models.md). |
| Python `abc` | Standard library | Abstract base class and abstract method definitions. |

## 4. Architecture Decision Log (ADL)

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/11/2026 | Defined the `LLMAdapter` contract for availability, model listing, and structured generation. | `LLMAdapter`, `check_availability()`, `list_models()`, `generate_structured()` (added) | [Use an LLM Service abstraction with pluggable LLM adapters](../../../../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md) |

## 5. References

- [LLM Service Technical System Specification](../../../systems/llm-service/overview.md)
- [Generation Models Module](models.md)
- [Generation Service Module](service.md)
- [Ollama Adapter Module](../../ollama-adapter/ollama-adapter.md)
- [LLM Component Technical Specification](../../../technical-specification.md)
