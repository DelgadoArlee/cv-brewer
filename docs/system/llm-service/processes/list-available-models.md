# List Available Models Process Document

## 1. Purpose / Summary

This process lists the models available on the configured LLM service so users can select which model handles language-processing tasks. It delegates model discovery to the configured LLM Adapter and returns the models the service provides.

## 2. Process Flow

    ```` mermaid
    flowchart TD
        A([Start]) --> B[Receive model listing request]
        B --> C[Request available models from configured adapter]
        C --> D{Listing succeeded?}
        D -->|Yes| E([Return available models])
        D -->|No| F([Report listing failure])
    ````

## 3. Rules

- **must** discover available models through the configured LLM Adapter
- **must** return an empty listing when the service provides no models
- **must** report adapter failures to the caller
- **must** not filter or rank models as part of this process

## 4. Constraints

- The process does not decide which model the user selects.
- The process does not install or download models.

## 5. References

- [LLM Service System Overview](../overview.md)
- [List Available Models Technical Process](../../../../llm/docs/systems/llm-service/processes/list-available-models.md)
- [List Service Models Process](../../llm-adapter/processes/list-service-models.md)
