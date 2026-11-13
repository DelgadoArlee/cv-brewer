# Generate Structured Response Adapter Technical Process

## 1. Purpose

Generate a structured response on the external Ollama service by sending prompt messages and a JSON Schema to the selected model.

## 2. Objective

Return the model's response parsed as a JSON object, with all failures translated into adapter errors.

## 3. Scope

- Send the generation request to the selected model with streaming disabled.
- Pass the JSON Schema through the structured-output format field.
- Parse the response message content as a JSON object.
- Translate failures into adapter errors.

The process does not construct or modify prompts and does not validate content against application schemas.

## 4. Rules & Constraints

- Prompt messages and the JSON Schema must be sent unchanged.
- Streaming must be disabled for the request.
- The JSON Schema must be passed through the structured-output format field.
- Response content that is not a JSON object must be reported as a response failure.
- Transport, timeout, response, and missing-model failures must be translated into adapter errors.

## 5. Workflow

### Diagram

```` mermaid
    flowchart TD
        A([Start]) --> B[Receive generation request]
        B --> C[Send messages and schema to selected model]
        C --> D{Generation succeeded?}
        D -->|No| E[Translate failure]
        E --> F([Raise adapter error])
        D -->|Yes| G[Parse response content]
        G --> H{Valid JSON object?}
        H -->|Yes| I([Return structured response])
        H -->|No| F
````

### Steps

1. Receive the generation request.
2. Send the prompt messages and JSON Schema to the selected model with streaming disabled.
3. Translate transport, timeout, response, and missing-model failures into adapter errors.
4. Parse the response message content as a JSON object.
5. Report content that is not a JSON object as a response failure.
6. Return the structured response.

## 6. Modules

- `app/llm/adapters/ollama/adapter.py` — Implements structured generation.
- `app/llm/llm_service/modules/generation/models.py` — Defines the generation request records.

## 7. Testing

### 7.1 Test Level

Process level.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| OGEN-001 | A service that returns valid JSON object content. | Generation is requested. | The parsed JSON object is returned. |
| OGEN-002 | A service that returns invalid JSON content. | Generation is requested. | An adapter response error is raised. |
| OGEN-003 | A request for a missing model. | Generation is requested. | An adapter model error is raised. |
| OGEN-004 | A service that cannot be reached. | Generation is requested. | An adapter connection error is raised. |
| OGEN-005 | A request that exceeds the read timeout. | Generation is requested. | An adapter timeout error is raised. |
| OGEN-006 | A service that returns a failed response. | Generation is requested. | An adapter response error is raised. |

### 7.3 Test Coverage

Tests must verify request payload construction, response parsing, and failure translation.

## 8. References

- [LLM Adapter Technical System Specification](../overview.md)
- [LLM Adapter System Overview](../../../../../../docs/system/llm-adapter/overview.md)
- [Generate Structured Response Technical Process](../../llm-service/processes/generate-structured-response.md)
- [Ollama Adapter Foundation ADR](../../../adr/11-11-26/ollama-adapter-foundation.md)
