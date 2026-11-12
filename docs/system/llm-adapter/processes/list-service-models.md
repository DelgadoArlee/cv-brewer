# List Service Models Process Document

## 1. Purpose / Summary

This process lists the models provided by the external LLM service. It communicates with the configured service endpoint, parses the model listing, translates failures, and returns the available models.

## 2. Process Flow

    ```` mermaid
    flowchart TD
        A([Start]) --> B[Receive model listing request]
        B --> C[Request model listing from external LLM service]
        C --> D{Listing succeeded?}
        D -->|Yes| E[Parse available models]
        E --> F([Return model listing])
        D -->|No| G[Translate failure]
        G --> H([Report listing failure])
    ````

## 3. Rules

- **must** request the model listing from the configured service endpoint
- **must** parse the service model listing into model records
- **must** return an empty listing when the service provides no models
- **must** translate communication, timeout, and response failures into adapter-level errors

## 4. Constraints

- The process does not filter or rank models.
- The process does not install or download models.

## 5. References

- [LLM Adapter System Overview](../overview.md)
- [List Service Models Technical Process](../../../../llm/docs/systems/llm-adapter/processes/list-service-models.md)
- [List Available Models Process](../../llm-service/processes/list-available-models.md)
