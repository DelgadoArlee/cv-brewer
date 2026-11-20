# Persist Resume Processing Step Process

## 1. Purpose / Summary

This process stores a resume processing step record through the Database Adapter so step-level execution details can be reviewed as part of a processing run. It preserves recorded values, run association, ordering and attempt information, embedded data, and identifier references.

## 2. Process Flow

````mermaid
flowchart TD
    A([Start]) --> B[Receive resume processing step record]
    B --> C[Map step record for persistence]
    C --> D[Store step record in transaction]
    D --> E{Stored successfully?}
    E -->|Yes| F([Step record stored])
    E -->|No| G([Report persistence failure])
````

## 3. Rules

- The adapter must store each accepted step record without changing its recorded values.
- The adapter must associate each step record with its owning processing run.
- The adapter must preserve `step_order`, `attempt_number`, and embedded `input`, `output`, `performance`, `error`, and `metadata` data.
- The adapter must treat `source_step_id` as an identifier reference rather than a required database relationship.
- The adapter must report persistence failures to the caller.
- The adapter must not create, update, or delete resume data or LLM activity log data as part of this process.

## 4. Constraints

- The process does not construct step records or execute processing steps.
- A step record must belong to exactly one processing run.

## 5. References

- [Database Adapter System Overview](/docs/system/database-adapter/overview.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Error Data Model](/docs/data/error.md)
- [Resume Processing Steps Table](/app/database/docs/sqlite/schemas/resume-processing-steps.md)
- [Persist Resume Processing Step Technical Process](/app/database/docs/system/database-adapter/processes/persist-resume-processing-step.md)
