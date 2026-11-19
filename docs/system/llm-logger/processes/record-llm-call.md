# Record LLM Call Process

## 1. Purpose / Summary

The record LLM call process observes an LLM generation call, measures its duration and memory use, and creates a complete activity log record from the request, response, or error before it is persisted.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B[Receive generation request]
    B --> C[Start measurement]
    C --> D[Delegate generation call]
    D --> E{Call succeeded?}
    E -->|Yes| F[Build success record with response and usage]
    E -->|Timeout| G[Build timeout record with error details]
    E -->|Failed| H[Build failed record with error details]
    F --> I[Deliver record to Logger Service]
    G --> I
    H --> I
    I --> J([Return original call result])
````

## 3. Rules

- The system must record structured generation calls only.
- The system must record the provider, model, system prompt, prompt, and generation parameters.
- The system must record response content, finish reason, and token usage when the call succeeds.
- The system must record error type and message when the call fails or times out.
- A timeout must be classified as a timeout; all other failures must be classified as failed.
- The system must not modify the request or the result of the observed call.
- The system must propagate the original result or error to the caller.

## 4. Constraints

- Availability checks and model listings must not be logged.
- Generation parameters must be recorded as null while the application does not supply them.
- Memory and duration measurement must apply only to the observed generation call.

## 5. References

- [LLM Activity Logging Feature Overview](/docs/features/llm-activity-logging.md)
- [LLM Logger System Overview](/docs/system/llm-logger/overview.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)
- [Record LLM Call Technical Process](/app/core/docs/system/llm-logger/processes/record-llm-call.md)
