# LLM Adapter Technical System Specification

## 1. Purpose

Defines the service-specific implementation of LLM operations for the LLM component. The adapter implements the Core-owned `LLMPort` contract and owns `httpx` communication, Ollama configuration, response parsing, and error translation.

## 2. Objective

- Implement the LLM Service operations for Ollama.
- Verify service availability through a lightweight service request.
- List models available on the service.
- Generate schema-constrained structured responses from the selected model.
- Translate communication, timeout, response, and model failures into the adapter error hierarchy.

## 3. Scope

### In Scope

- Ollama adapter package under `app/llm/adapters/ollama/`.
- Ollama configuration.
- HTTP communication for availability verification, model listing, and structured generation.
- Response parsing and adapter error translation.

### Out of Scope

- Application-level operation definitions, which belong to the Core-owned LLM Service.
- Prompt construction and JSON Schema selection.
- Schema validation of generated content.
- CLI and workflow behavior.

## 4. Rules & Constraints

- The adapter must use a synchronous `httpx` client.
- Availability must be verified through a lightweight service request.
- Models must be listed from the service model listing.
- Structured generation must send the prompt messages and JSON Schema unchanged, with streaming disabled.
- Structured generation must pass the JSON Schema through the structured-output format field.
- Response content must be parsed as a JSON object.
- `httpx` transport, timeout, and response failures must be translated through the adapter error hierarchy.
- Missing models must be reported as adapter model errors.

## 5. Process

| Process | Description | Specification |
| --- | --- | --- |
| Verify Service Availability | Verifies the external Ollama service is reachable. | [Verify Service Availability](/app/llm/docs/system/llm-adapter/processes/verify-service-availability.md) |
| List Service Models | Lists the models provided by the Ollama service. | [List Service Models](/app/llm/docs/system/llm-adapter/processes/list-service-models.md) |
| Generate Structured Response | Sends a generation request to the selected model and returns the parsed JSON object. | [Generate Structured Response](/app/llm/docs/system/llm-adapter/processes/generate-structured-response.md) |
| Log Generation Call | Measures a generation call and reports its outcome to the LLM logger. | [Log Generation Call](/app/llm/docs/system/llm-adapter/processes/log-generation-call.md) |

## 6. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `httpx` | External library | Synchronous HTTP client for Ollama communication. |
| `LLMPort` | Core-owned interface | Defines the adapter contract implemented by the Ollama adapter. |
| `StructuredGenerationRequest`, `ChatMessage`, `ModelInfo` | Core-owned records | Application-level data handled by the adapter. |

## 7. Test Cases

| Test Case ID | Scenario | Expected Result | Related Rule |
| --- | --- | --- | --- |
| LLM-ADP-001 | Verify availability against a reachable service. | The service is reported available. | Availability rule |
| LLM-ADP-002 | Verify availability against an unreachable service. | The service is reported unavailable. | Availability rule |
| LLM-ADP-003 | List models from a service with models. | The model records are returned. | Model listing rule |
| LLM-ADP-004 | List models from a service with no models. | An empty listing is returned. | Model listing rule |
| LLM-ADP-005 | Generate a structured response with valid JSON content. | The parsed JSON object is returned. | Structured generation rule |
| LLM-ADP-006 | Generate a structured response with invalid JSON content. | An adapter response failure is raised. | Response parsing rule |
| LLM-ADP-007 | Generate with a missing model. | An adapter model failure is raised. | Missing model rule |
| LLM-ADP-008 | Generate while the service is unreachable. | An adapter connection failure is raised. | Error translation rule |
| LLM-ADP-009 | Generate while the request times out. | An adapter timeout failure is raised. | Error translation rule |
| LLM-ADP-010 | Receive a failed service response. | An adapter response failure is raised. | Error translation rule |

## 8. Diagrams

````mermaid
flowchart LR
    Service[LLMService] --> Port[LLMPort]
    Port --> Adapter[OllamaAdapter]
    Adapter --> Client[httpx.Client]
    Client --> Ollama[(Ollama Service)]
````

## 9. Architecture Decision Log

| ADR | Decision Summary |
| --- | --- |
| [Retain LLM Adapters as the LLM component boundary](/app/llm/docs/adr/11-14-26/adapter-only-boundary.md) | Keep adapters in the LLM component and implement the Core-owned `LLMPort` contract. |
| [Establish the Ollama adapter foundation](/app/llm/docs/adr/11-11-26/ollama-adapter-foundation.md) | Use synchronous `httpx`, adapter-local configuration and errors, and structured outputs through the chat endpoint. |
| [Use an LLM Service abstraction with pluggable LLM adapters](/docs/adr/Architecture/2026-11-11/llm-service-abstraction.md) | Define application-level LLM operations behind an LLM Service that adapters implement. |
| [Move the LLM Service into Core](/docs/adr/Architecture/2026-11-14/llm-service-to-core.md) | Own application-level language-model operations in Core while LLM retains adapters. |

## 10. Data

The adapter handles Core-owned records defined in `app/core/services/llm/models.py`.

## 11. References

- [LLM Adapter System Overview](/docs/system/llm-adapter/overview.md)
- [LLM Component Technical Specification](/app/llm/docs/technical-specification.md)
- `app/llm/adapters/ollama/adapter.py` — Implements Ollama communication.
- `app/core/services/llm/port.py` — Defines the adapter contract.
- [Retain LLM Adapters as the LLM component boundary](/app/llm/docs/adr/11-14-26/adapter-only-boundary.md)
- [Ollama Adapter Foundation ADR](/app/llm/docs/adr/11-11-26/ollama-adapter-foundation.md)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
