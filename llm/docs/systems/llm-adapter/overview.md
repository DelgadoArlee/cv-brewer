# LLM Adapter Technical System Specification

## 1. Purpose

Defines the service-specific implementation of LLM operations for the LLM component. The adapter owns `httpx` communication, Ollama configuration, response parsing, and error translation.

## 2. Objective

- Implement the LLM Service operations for Ollama.
- Verify service availability through a lightweight service request.
- List models available on the service.
- Generate schema-constrained structured responses from the selected model.
- Translate communication, timeout, response, and model failures into the adapter error hierarchy.

## 3. Scope

### In Scope

- Ollama adapter package under `llm/src/llm/adapters/ollama/`.
- Ollama configuration.
- HTTP communication for availability verification, model listing, and structured generation.
- Response parsing and adapter error translation.

### Out of Scope

- Application-level operation definitions.
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
| Verify Service Availability | Verifies the external Ollama service is reachable. | [Verify Service Availability](processes/verify-service-availability.md) |
| List Service Models | Lists the models provided by the Ollama service. | [List Service Models](processes/list-service-models.md) |
| Generate Structured Response | Sends a generation request to the selected model and returns the parsed JSON object. | [Generate Structured Response](processes/generate-structured-response.md) |

## 6. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `httpx` | External library | Synchronous HTTP client for Ollama communication. |
| `LLMAdapter` | Internal interface | Defines the adapter contract implemented by the Ollama adapter. |
| `StructuredGenerationRequest`, `ChatMessage`, `ModelInfo` | Internal records | Application-level data handled by the adapter. |

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
    Service[LLMService] --> Port[LLMAdapter]
    Port --> Adapter[OllamaAdapter]
    Adapter --> Client[httpx.Client]
    Client --> Ollama[(Ollama Service)]
````

## 9. Architecture Decision Log

| ADR | Decision Summary |
| --- | --- |
| [Establish the Ollama adapter foundation](../../adr/11-11-26/ollama-adapter-foundation.md) | Use synchronous `httpx`, adapter-local configuration and errors, and structured outputs through the chat endpoint. |
| [Use an LLM Service abstraction with pluggable LLM adapters](../../../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md) | Define application-level LLM operations behind an LLM Service that adapters implement. |

## 10. Data

The adapter handles application-level records documented in [Generation Models Module](../../modules/llm-service/generation/models.md).

## 11. References

- [LLM Adapter System Overview](../../../../docs/system/llm-adapter/overview.md)
- [LLM Component Technical Specification](../../technical-specification.md)
- [Ollama Adapter Module](../../modules/ollama-adapter/ollama-adapter.md)
- [Generation Adapter Module](../../modules/llm-service/generation/adapter.md)
- [Ollama Adapter Foundation ADR](../../adr/11-11-26/ollama-adapter-foundation.md)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
