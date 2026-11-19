# Persist LLM Log Process

## 1. Purpose / Summary

The persist LLM log process stores a completed LLM activity log record in the embedded database and makes stored records available for review.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B[Receive LLM activity log record]
    B --> C[Validate record is complete]
    C --> D{Valid?}
    D -->|No| E[Reject record]
    D -->|Yes| F[Store record]
    F --> G{Storage succeeded?}
    G -->|No| H[Report persistence failure]
    G -->|Yes| I([Record stored])
````

## 3. Rules

- The system must store each accepted record without changing its values.
- The system must preserve status values of success, failed, and timeout.
- The system must report persistence failures to the caller.
- The system must return stored records without interpreting their contents.
- The system must not create, update, or delete resume data.

## 4. Constraints

- Storage is limited to LLM activity log records.
- Listing is limited to returning stored LLM activity log records.

## 5. References

- [LLM Activity Logging Feature Overview](/docs/features/llm-activity-logging.md)
- [LLM Logger System Overview](/docs/system/llm-logger/overview.md)
- [Database Service System Overview](/docs/system/database-service/overview.md)
- [Persist LLM Log Technical Process](/app/database/docs/system/database-adapter/processes/persist-llm-log.md)
