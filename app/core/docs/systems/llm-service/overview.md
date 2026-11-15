# LLM Service Technical System Specification

## 1. Purpose

Defines the application-level LLM operations exposed by the Core application layer. The LLM Service owns generation request structures and operation definitions while delegating all communication to an LLM Adapter.

## 2. Objective

- Provide availability, model discovery, and structured generation operations without service-specific coupling.
- Define the records used across the service boundary.
- Verify generation requests are complete before delegation.
- Delegate all communication work to a port implemented by the LLM Adapter system.

## 3. Scope

### In Scope

- LLM service module under `app/core/services/llm/`.
- Application-level generation request, prompt message, and model record definitions.
- LLM port abstraction.
- LLM service operations for availability, model listing, and structured generation.

### Out of Scope

- Ollama HTTP communication, configuration, and error translation.
- Prompt construction and JSON Schema selection.
- Schema validation of generated content.
- CLI workflows and LLM selection presentation.

## 4. Rules & Constraints

- The service must not import `httpx` or Ollama-specific modules.
- All communication must go through the `LLMPort` abstraction.
- Generation requests must provide a model, at least one prompt message, and a JSON Schema.
- Incomplete generation requests must be rejected before the adapter is called.
- Model listings must return an empty list when the service provides no models.
- Adapter failures must propagate to the caller.

## 5. Process

| Process | Description | Specification |
| --- | --- | --- |
| Check LLM Availability | Verifies the configured LLM service is reachable through the adapter. | [Check LLM Availability](processes/check-llm-availability.md) |
| List Available Models | Returns the models provided by the configured LLM service. | [List Available Models](processes/list-available-models.md) |
| Generate Structured Response | Submits a complete generation request and returns the structured response. | [Generate Structured Response](processes/generate-structured-response.md) |

## 6. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `LLMPort` | Internal interface | Accepts application-level LLM operations for availability, model listing, and structured generation. |
| LLM Adapter | Internal system | Provides the concrete adapter implementation. |

## 7. Test Cases

| Test Case ID | Scenario | Expected Result | Related Rule |
| --- | --- | --- | --- |
| LLM-SVC-001 | Check availability through the adapter. | The adapter availability outcome is returned. | Availability operation |
| LLM-SVC-002 | List models through the adapter. | The adapter model listing is returned. | Model listing operation |
| LLM-SVC-003 | List models when the service provides none. | An empty listing is returned. | Empty listing rule |
| LLM-SVC-004 | Generate a structured response with a complete request. | The request is delegated and the structured response is returned. | Generation operation |
| LLM-SVC-005 | Generate with a request missing a model, messages, or a JSON Schema. | The request is rejected before the adapter is called. | Complete request rule |
| LLM-SVC-006 | Generate while the adapter reports a failure. | The adapter failure is reported to the caller. | Failure propagation rule |

## 8. Diagrams

````mermaid
flowchart LR
    Caller[Application Caller] --> Service[LLMService]
    Service --> Port[LLMPort]
    Port --> Adapter[Ollama Adapter]
````

## 9. Architecture Decision Log

| ADR | Decision Summary |
| --- | --- |
| [Establish the LLM service package](../../adr/11-14-26/llm-service-package.md) | Place all LLM-specific records, the `LLMPort` contract, and service operations under `app/core/services/llm/`. |
| [Move the LLM Service into Core](../../../../../docs/adr/Architecture/2026-11-14/llm-service-to-core.md) | Own application-level language-model operations in Core while LLM retains adapters. |
| [Retain LLM Adapters as the LLM Component Boundary](../../../../llm/docs/adr/11-14-26/adapter-only-boundary.md) | Keep adapters in LLM and implement the Core-owned `LLMPort` contract. |
| [Use an LLM Service abstraction with pluggable LLM adapters](../../../../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md) | Define application-level LLM operations behind an LLM Service that adapters implement. |

## 10. Data

The service defines generation request records in `app/core/services/llm/models.py`.

## 11. References

- [LLM Service System Overview](../../../../../docs/system/llm-service/overview.md)
- [Core Component Technical Specification](../../technical-specification.md)
- `app/core/services/llm/models.py` — Defines generation request records.
- `app/core/services/llm/port.py` — Defines the adapter contract.
- `app/core/services/llm/service.py` — Implements application-level LLM operations.
- [Move the LLM Service into Core](../../../../../docs/adr/Architecture/2026-11-14/llm-service-to-core.md)
- [Establish the LLM service package](../../adr/11-14-26/llm-service-package.md)
- [Retain LLM Adapters as the LLM Component Boundary](../../../../llm/docs/adr/11-14-26/adapter-only-boundary.md)
- [Use an LLM Service abstraction with pluggable LLM adapters](../../../../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md)
