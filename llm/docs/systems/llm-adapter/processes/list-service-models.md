# List Service Models Technical Process

## 1. Purpose

List the models provided by the external Ollama service by requesting the service model listing.

## 2. Objective

Return the model records available on the configured service.

## 3. Scope

- Request the model listing from the configured Ollama service.
- Parse the listing into model records.
- Translate failures into adapter errors.

The process does not filter or rank models and does not install or download models.

## 4. Rules & Constraints

- The listing must be requested from the service model listing endpoint.
- An empty listing must be returned when the service provides no models.
- Transport, timeout, and response failures must be translated into adapter errors.

## 5. Workflow

### Diagram

```` mermaid
    flowchart TD
        A([Start]) --> B[Receive model listing request]
        B --> C[Request service model listing]
        C --> D{Listing succeeded?}
        D -->|Yes| E[Parse model records]
        E --> F([Return model listing])
        D -->|No| G[Translate failure]
        G --> H([Raise adapter error])    
````

### Steps

1. Receive the model listing request.
2. Request the model listing from the configured Ollama service.
3. Translate transport, timeout, and response failures into adapter errors.
4. Parse the service listing into model records.
5. Return the model listing.

## 6. Modules

- `llm/src/llm/adapters/ollama/adapter.py` — Implements the model listing operation.

## 7. Testing

### 7.1 Test Level

Process level.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| MODELS-001 | A service that lists models. | Models are listed. | The model records are returned. |
| MODELS-002 | A service that lists no models. | Models are listed. | An empty listing is returned. |
| MODELS-003 | A service that cannot be reached. | Models are listed. | An adapter connection error is raised. |
| MODELS-004 | A service that returns a failed response. | Models are listed. | An adapter response error is raised. |

### 7.3 Test Coverage

Tests must verify listing, empty listing, and failure translation.

## 8. References

- [LLM Adapter Technical System Specification](../overview.md)
- [LLM Adapter System Overview](../../../../../docs/system/llm-adapter/overview.md)
- [List Available Models Technical Process](../../llm-service/processes/list-available-models.md)
