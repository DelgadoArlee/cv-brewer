# Generate Structured Response Adapter Process Document

## 1. Purpose / Summary

This process generates a structured response on the external LLM service. It sends the prompt messages and JSON Schema to the selected model, requests a schema-constrained JSON response, parses the response content, and translates failures into adapter-level errors.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B[Receive generation request]
    B --> C[Send prompt messages and schema to selected model]
    C --> D{Generation succeeded?}
    D -->|Yes| E[Parse structured response content]
    E --> F{Valid JSON object?}
    F -->|Yes| G([Return structured response])
    F -->|No| H[Translate response failure]
    D -->|No| I[Translate failure]
    H --> J([Report response failure])
    I --> J
````

## 3. Rules

- **must** send the prompt messages and JSON Schema exactly as provided by the LLM Service
- **must** request a schema-constrained JSON-formatted response
- **must** parse the response content into a JSON object
- **must** report invalid structured response content as a response failure
- **must** translate communication, timeout, response, and model failures into adapter-level errors

## 4. Constraints

- The process does not construct or modify prompts.
- The process does not validate content against application schemas.
- The process does not store generated content.

## 5. References

- [LLM Adapter System Overview](../overview.md)
- [Generate Structured Response Technical Process](../../../../app/llm/docs/systems/llm-adapter/processes/generate-structured-response.md)
- [Generate Structured Response Process](../../llm-service/processes/generate-structured-response.md)
