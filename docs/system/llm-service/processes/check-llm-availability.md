# Check LLM Availability Process Document

## 1. Purpose / Summary

This process verifies that the configured LLM service is reachable so processing workflows can report LLM connection problems before generation is attempted. It delegates the availability check to the configured LLM Adapter and reports whether the service is available.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B[Receive availability request]
    B --> C[Request availability check from configured adapter]
    C --> D{Service reachable?}
    D -->|Yes| E([Report service available])
    D -->|No| F([Report service unavailable])
````

## 3. Rules

- **must** perform the availability check through the configured LLM Adapter
- **must** report an unavailable outcome when the LLM service cannot be reached
- **must** report adapter failures to the caller
- **must** not construct prompts as part of this process
- **must** not attempt generation as part of this process

## 4. Constraints

- The process does not decide how unavailable services are presented to the user.
- The process does not verify that a specific model is installed.

## 5. References

- [LLM Service System Overview](../overview.md)
- [Check LLM Availability Technical Process](../../../../app/llm/docs/systems/llm-service/processes/check-llm-availability.md)
- [Verify Service Availability Process](../../llm-adapter/processes/verify-service-availability.md)
