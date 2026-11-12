# Generate Structured Response Process Document

## 1. Purpose / Summary

This process generates a structured response by submitting a prompt and a JSON Schema to the selected model through the configured LLM Adapter. It verifies the generation request is complete, delegates generation to the adapter, and returns the structured response so the Core can validate it against the application schema in a separate step.

## 2. Process Flow

    ```` mermaid
    flowchart TD
        A([Start]) --> B[Receive generation request]
        B --> C{Request complete?}
        C -->|No| D([Reject incomplete request])
        C -->|Yes| E[Submit prompt and schema to selected model via adapter]
        E --> F{Generation succeeded?}
        F -->|Yes| G([Return structured response])
        F -->|No| H([Report generation failure])
    ````

## 3. Rules

- **must** require a model, at least one prompt message, and a JSON Schema in every generation request
- **must** reject incomplete generation requests before the adapter is called
- **must** delegate generation to the configured LLM Adapter
- **must** report adapter failures to the caller
- **must** return the structured response regardless of content quality; validation happens separately

## 4. Constraints

- The process does not construct prompts or select JSON Schemas; the Core provides them.
- The process does not validate the generated content against application schemas.
- The process does not store generated content.

## 5. References

- [LLM Service System Overview](../overview.md)
- [Generate Structured Response Technical Process](../../../../llm/docs/systems/llm-service/processes/generate-structured-response.md)
- [Generate Structured Response Adapter Process](../../llm-adapter/processes/generate-structured-response.md)
- [Job Description Parsing Process](../../resume-generation/processes/2-job-description-parsing.md)
- [Resume Content Generation Process](../../resume-generation/processes/4-resume-content-generation.md)
