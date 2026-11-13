# Generate Structured Response Technical Process

## 1. Purpose

Generate a structured response by verifying a generation request is complete and delegating structured generation to the configured LLM Adapter.

## 2. Objective

Return the structured response produced by the selected model so the Core can validate it against the application schema in a separate step.

## 3. Scope

- Receive a generation request.
- Verify the request provides a model, at least one prompt message, and a JSON Schema.
- Delegate generation to the configured adapter.
- Return the structured response.

The process does not construct prompts, select schemas, or validate generated content.

## 4. Rules & Constraints

- Generation requests missing a model, prompt messages, or a JSON Schema must be rejected before the adapter is called.
- The request must be delegated unchanged; the service must not modify prompts or schemas.
- Adapter failures must propagate to the caller.
- The structured response must be returned regardless of content quality; validation happens separately.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B[Receive generation request]
    B --> C{Request complete?}
    C -->|No| D([Reject incomplete request])
    C -->|Yes| E[Delegate generation to adapter]
    E --> F([Return structured response])
````

### Steps

1. Receive the generation request.
2. Verify the request provides a model, at least one prompt message, and a JSON Schema.
3. Reject incomplete requests before communication.
4. Delegate the complete request to the configured adapter.
5. Return the structured response.

## 6. Modules

- `llm/src/llm/llm_service/modules/generation/service.py` — Implements request verification and delegation.
- `llm/src/llm/llm_service/modules/generation/models.py` — Defines the generation request records.

## 7. Testing

### 7.1 Test Level

Process level.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| GEN-001 | A complete generation request. | Generation is requested. | The adapter receives the request unchanged and the structured response is returned. |
| GEN-002 | A request missing a model. | Generation is requested. | The request is rejected and the adapter is not called. |
| GEN-003 | A request with no prompt messages. | Generation is requested. | The request is rejected and the adapter is not called. |
| GEN-004 | A request without a JSON Schema. | Generation is requested. | The request is rejected and the adapter is not called. |

### 7.3 Test Coverage

Tests must verify completeness rejection and unchanged delegation.

## 8. References

- [LLM Service Technical System Specification](../overview.md)
- [LLM Service System Overview](../../../../../docs/system/llm-service/overview.md)
- [Generate Structured Response Adapter Technical Process](../../llm-adapter/processes/generate-structured-response.md)
