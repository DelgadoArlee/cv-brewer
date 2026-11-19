# Log Generation Call Technical Process

## 1. Purpose

Wrap a structured generation call so its outcome and measurements are logged without changing behavior.

## 2. Objective

Provide provider-agnostic logging around any LLM port implementation.

## 3. Scope

- Delegate generation, availability, and model listing calls.
- Measure and log structured generation calls.
- Return or re-raise the wrapped adapter's outcome unchanged.

The process does not persist records or define application log records.

## 4. Rules & Constraints

- The wrapper must implement the Core-owned LLM port.
- The wrapper must delegate unchanged requests to the wrapped adapter.
- Only `generate_structured` calls may be logged.
- The provider name must be supplied at construction.
- The original result or exception must be returned or re-raised unchanged.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B{Operation}
    B -->|Generate| C[Start measurement]
    C --> D[Delegate generation]
    D --> E{Call outcome}
    E --> F[Report outcome to logger]
    F --> G[Return or re-raise outcome]
    B -->|Other| H[Delegate unchanged]
    H --> G
    G --> I([End])
````

### Steps

1. Receive the port operation.
2. For non-generation operations, delegate unchanged.
3. For generation, start measurement and delegate the request.
4. Report the result or error with measurements to the LLM logger.
5. Return the result or re-raise the original error.

## 6. Modules

- `app/llm/adapters/logging/adapter.py` — Implements the logging LLM port wrapper.
- `app/core/services/llm/logger.py` — Builds LLM activity log records.
- `app/llm/adapters/ollama/adapter.py` — Provides provider-specific generation results.

## 7. Testing

### 7.1 Test Level

Process level.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| LOG-ADP-001 | A successful wrapped generation. | Generation is requested. | The result is returned and a success record is reported. |
| LOG-ADP-002 | A failing wrapped generation. | Generation is requested. | The error is re-raised and a failure record is reported. |
| LOG-ADP-003 | A non-generation operation. | The operation is requested. | It is delegated without logging. |

### 7.3 Test Coverage

Tests must verify unchanged delegation and unchanged outcomes.

### 7.4 Test Organization

Tests reside under `tests/llm/adapters/logging/`.

### 7.5 Test Dependencies

Use test doubles for the wrapped port and logger.

### 7.6 Testing Rules Compliance

Tests verify observable behavior and use test doubles only for external boundaries.

## 8. References

- [Log Generation Call Process](/docs/system/llm-adapter/processes/log-generation-call.md)
- [LLM Adapter Technical System Specification](/app/llm/docs/system/llm-adapter/overview.md)
- [Capture LLM Logs at the Adapter Boundary](/app/llm/docs/adr/11-19-26/logging-adapter.md)
