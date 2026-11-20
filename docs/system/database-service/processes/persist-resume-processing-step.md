# Persist Resume Processing Step Process

## 1. Purpose / Summary

The persist resume processing step process stores a resume processing step record associated with a processing run so step-level execution details, input/output summaries, performance measurements, metadata, and embedded error data can be reviewed later. It accepts a complete step record and delegates persistence to the configured database adapter.

## 2. Process Flow

````mermaid
flowchart TD
    A([Start]) --> B[Receive resume processing step record]
    B --> C[Validate step record is complete]
    C --> D{Valid?}
    D -->|No| E[Log persistence failure]
    D -->|Yes| F[Store step record]
    F --> G{Storage succeeded?}
    G -->|No| H[Log persistence failure]
    G -->|Yes| I([Step record stored])
````

## 3. Rules

- The system must store each accepted step record without changing its recorded values.
- The system must associate each step record with its owning processing run.
- The system must preserve step ordering, attempt information, and embedded `input`, `output`, `performance`, `error`, and `metadata` data.
- The system must treat `source_step_id` as an identifier reference rather than a required database relationship.
- The system must report persistence failures through standard logging and must not stop resume processing.
- The system must not create, update, or delete resume data or LLM activity log data as part of this process.

## 4. Constraints

- The process records processing step execution data only; it does not execute processing steps.
- Step records may be stored for successful, failed, skipped, or otherwise recorded step outcomes according to the owning run.
- A step record must belong to exactly one processing run.

## 5. References

- [Database Service System Overview](/docs/system/database-service/overview.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Error Data Model](/docs/data/error.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)
- [Persist Resume Processing Step Technical Process](/app/database/docs/system/database-adapter/processes/persist-resume-processing-step.md)
