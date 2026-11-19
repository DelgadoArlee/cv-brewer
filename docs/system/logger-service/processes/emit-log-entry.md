# Emit Log Entry Process

## 1. Purpose / Summary

The emit log entry process delivers a structured log record to every configured destination so activity information is recorded consistently and independently of any single storage mechanism.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B[Receive structured log record]
    B --> C{Destinations configured?}
    C -->|No| D([Complete without delivery])
    C -->|Yes| E[Deliver record to each destination]
    E --> F{Delivery succeeded?}
    F -->|Yes| G([Complete])
    F -->|No| H[Report delivery failure]
    H --> I([Stop])
````

## 3. Rules

- The system must deliver each accepted log record to every configured destination.
- The system must not change the contents of the log record during delivery.
- The system must complete successfully when no destinations are configured.
- The system must report a delivery failure to the caller.
- The system must not create log records for application activities on its own.

## 4. Constraints

- The process is limited to delivery; it does not decide which activities are logged.
- The process must not depend on a specific destination technology.

## 5. References

- [LLM Activity Logging Feature Overview](/docs/features/llm-activity-logging.md)
- [Logger Service System Overview](/docs/system/logger-service/overview.md)
- [Emit Log Entry Technical Process](/app/core/docs/system/logger-service/processes/emit-log-entry.md)
