# Verify Service Availability Technical Process

## 1. Purpose

Verify that the external Ollama service is reachable by performing a lightweight service request.

## 2. Objective

Report whether the Ollama service is available without loading a model or performing generation.

## 3. Scope

- Send a lightweight service request to the configured Ollama service.
- Report the availability outcome.
- Translate transport failures into an unavailable outcome.

The process does not verify installed models and does not define application-level availability operations.

## 4. Rules & Constraints

- Availability must be verified through a lightweight service request.
- Transport and timeout failures must result in an unavailable outcome.
- The process must not load a model or perform generation.

## 5. Workflow

### Diagram

```` mermaid
    flowchart TD
        A([Start]) --> B[Receive availability check]
        B --> C[Send lightweight service request]
        C --> D{Response received?}
        D -->|Yes| E([Report service available])
        D -->|No| F([Report service unavailable])
````

### Steps

1. Receive the availability check.
2. Send a lightweight service request to the configured Ollama service.
3. Report the service as available when a response is received.
4. Report the service as unavailable when communication fails.

## 6. Modules

- `app/llm/adapters/ollama/adapter.py` — Implements the availability verification.

## 7. Testing

### 7.1 Test Level

Process level.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| AVAIL-001 | A service that responds to the lightweight request. | Availability is verified. | The service is reported available. |
| AVAIL-002 | A service that cannot be reached. | Availability is verified. | The service is reported unavailable. |
| AVAIL-003 | A request that times out. | Availability is verified. | The service is reported unavailable. |

### 7.3 Test Coverage

Tests must verify reachable, unreachable, and timeout outcomes.

## 8. References

- [LLM Adapter Technical System Specification](../overview.md)
- [LLM Adapter System Overview](../../../../../../docs/system/llm-adapter/overview.md)
- [Check LLM Availability Technical Process](../../llm-service/processes/check-llm-availability.md)
