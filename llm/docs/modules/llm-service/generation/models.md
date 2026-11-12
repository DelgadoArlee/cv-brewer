# Generation Models Module Technical Specification

## 1. Purpose

Defines the application-level records used across the LLM Service boundary. The module owns prompt message, model, and structured generation request records shared by the LLM Service and LLM Adapter implementations.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `ChatMessage` | Dataclass | Represents a single prompt message sent to a model. | `role: str` – Message role, such as `system`, `user`, or `assistant`. `content: str` – Message content. | `ChatMessage` instance. |
| `ModelInfo` | Dataclass | Represents a model available on the configured LLM service. | `name: str` – Model name used for generation requests. | `ModelInfo` instance. |
| `StructuredGenerationRequest` | Dataclass | Represents a structured generation request submitted to a model. | `model: str` – Model name that handles the request. `messages: list[ChatMessage]` – Prompt messages sent to the model. `json_schema: dict[str, Any]` – JSON Schema constraining the response. | `StructuredGenerationRequest` instance. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| Python `dataclasses` | Standard library | Frozen record definitions. |

## 4. Architecture Decision Log (ADL)

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/11/2026 | Defined the shared generation request, prompt message, and model records for the LLM Service boundary. | `ChatMessage`, `ModelInfo`, `StructuredGenerationRequest` (added) | [Use an LLM Service abstraction with pluggable LLM adapters](../../../../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md) |

## 5. References

- [LLM Service Technical System Specification](../../../systems/llm-service/overview.md)
- [Generation Adapter Module](adapter.md)
- [Generation Service Module](service.md)
- [LLM Component Technical Specification](../../../technical-specification.md)
