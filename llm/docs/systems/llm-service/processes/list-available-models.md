# List Available Models Technical Process

## 1. Purpose

Return the models available on the configured LLM service by delegating model discovery to the configured LLM Adapter.

## 2. Objective

Provide the model listing used for LLM selection.

## 3. Scope

- Receive a model listing request.
- Delegate model discovery to the configured adapter.
- Return the available models.

The process does not filter, rank, install, or download models.

## 4. Rules & Constraints

- The listing must be delegated to the configured adapter.
- An empty listing must be returned when the service provides no models.
- Adapter failures must propagate to the caller.

## 5. Workflow

### Diagram

    ```` mermaid
    flowchart TD
        A([Start]) --> B[Receive model listing request]
        B --> C[Delegate model discovery to adapter]
        C --> D([Return available models])
    ````

### Steps

1. Receive the model listing request.
2. Delegate model discovery to the configured adapter.
3. Return the available models.

## 6. Modules

- `llm/src/llm/llm_service/modules/generation/service.py` — Implements the model listing operation.

## 7. Testing

### 7.1 Test Level

Process level.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| LIST-001 | A configured adapter that provides models. | Models are listed. | The model records are returned. |
| LIST-002 | A configured adapter that provides no models. | Models are listed. | An empty listing is returned. |

### 7.3 Test Coverage

Tests must verify delegation and empty-listing behavior.

## 8. References

- [LLM Service Technical System Specification](../overview.md)
- [LLM Service System Overview](../../../../../docs/system/llm-service/overview.md)
- [List Service Models Technical Process](../../llm-adapter/processes/list-service-models.md)
