# Log Generation Call Process

## 1. Purpose / Summary

The log generation call process observes a language-model generation call at the adapter boundary, records its outcome, and leaves the original call result or error unchanged.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B[Receive generation request]
    B --> C[Start measurement]
    C --> D[Delegate to wrapped adapter]
    D --> E[Stop measurement]
    E --> F[Record call outcome]
    F --> G[Return result or propagate error]
    G --> H([End])
````

## 3. Rules

- The system must perform measurement only around structured generation calls.
- The system must record the request, result or error, and measurements.
- The system must not change the request passed to the wrapped adapter.
- The system must not change the result or error returned to the caller.

## 4. Constraints

- Availability checks and model listings must not be logged.
- The logging boundary must not define application records.

## 5. References

- [LLM Activity Logging Feature Overview](/docs/features/llm-activity-logging.md)
- [LLM Adapter System Overview](/docs/system/llm-adapter/overview.md)
- [Log Generation Call Technical Process](/app/llm/docs/system/llm-adapter/processes/log-generation-call.md)
