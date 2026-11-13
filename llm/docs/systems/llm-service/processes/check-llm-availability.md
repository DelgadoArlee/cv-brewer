# Check LLM Availability Technical Process

## 1. Purpose

Verify that the configured LLM service is reachable by delegating an availability check to the configured LLM Adapter.

## 2. Objective

Report whether the LLM service is available so processing workflows can report connection problems before generation is attempted.

## 3. Scope

- Receive an availability request.
- Delegate the availability check to the configured adapter.
- Return the availability outcome.

The process does not verify that a specific model is installed and does not perform generation.

## 4. Rules & Constraints

- The check must be delegated to the configured adapter.
- Adapter failures must not be swallowed; availability outcomes must reflect the adapter result.
- The process must not construct prompts.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B[Receive availability request]
    B --> C[Delegate availability check to adapter]
    C --> D([Return availability outcome])
````

### Steps

1. Receive the availability request.
2. Delegate the availability check to the configured adapter.
3. Return the availability outcome.

## 6. Modules

- `llm/src/llm/llm_service/modules/generation/service.py` — Implements the availability operation.

## 7. Testing

### 7.1 Test Level

Process level.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| CHECK-001 | A configured adapter that reports the service reachable. | Availability is checked. | The service is reported available. |
| CHECK-002 | A configured adapter that reports the service unreachable. | Availability is checked. | The service is reported unavailable. |

### 7.3 Test Coverage

Tests must verify delegation and outcome reporting.

## 8. References

- [LLM Service Technical System Specification](../overview.md)
- [LLM Service System Overview](../../../../../docs/system/llm-service/overview.md)
- [Verify Service Availability Technical Process](../../llm-adapter/processes/verify-service-availability.md)
