# Verify Service Availability Process Document

## 1. Purpose / Summary

This process verifies that the external LLM service is reachable by performing a lightweight service request. It communicates with the configured service endpoint, translates communication failures, and reports whether the service is available.

## 2. Process Flow

    ```` mermaid
    flowchart TD
        A([Start]) --> B[Receive availability check]
        B --> C[Send service request to external LLM service]
        C --> D{Response received?}
        D -->|Yes| E([Report service available])
        D -->|No| F[Translate communication failure]
        F --> G([Report service unavailable])
    ````

## 3. Rules

- **must** verify availability through a lightweight service request
- **must** report an unavailable outcome when the service cannot be reached
- **must** translate communication and timeout failures into adapter-level errors
- **must** not load a model or perform generation as part of this process

## 4. Constraints

- The process does not define application-level availability operations.
- The process does not verify that a specific model is installed.

## 5. References

- [LLM Adapter System Overview](../overview.md)
- [Verify Service Availability Technical Process](../../../../llm/docs/systems/llm-adapter/processes/verify-service-availability.md)
- [Check LLM Availability Process](../../llm-service/processes/check-llm-availability.md)
