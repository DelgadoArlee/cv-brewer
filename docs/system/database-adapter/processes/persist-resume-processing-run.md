# Persist Resume Processing Run Process

## 1. Purpose / Summary

This process stores a resume processing run record through the Database Adapter so execution outcome, timing, summary, performance, resume identifier references, and embedded error data can be reviewed later. It preserves recorded values and maintains the separation between processing execution logs and resume records.

## 2. Process Flow

````mermaid
flowchart TD
    A([Start]) --> B[Receive resume processing run record]
    B --> C[Map run record for persistence]
    C --> D[Store run record in transaction]
    D --> E{Stored successfully?}
    E -->|Yes| F([Run record stored])
    E -->|No| G([Report persistence failure])
````

## 3. Rules

- The adapter must store each accepted run record without changing its recorded values.
- The adapter must preserve `resume_id` and `matched_resume_id` as identifier references without creating database relationships to resume records.
- The adapter must persist embedded `summary`, `performance`, and `error` data according to the SQLite schema mapping.
- The adapter must report persistence failures to the caller.
- The adapter must not create, update, or delete resume data as part of this process.

## 4. Constraints

- The process does not construct run records or control resume-processing workflow decisions.
- Run records may exist for outcomes that do not produce a stored parsed resume.

## 5. References

- [Database Adapter System Overview](/docs/system/database-adapter/overview.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Error Data Model](/docs/data/error.md)
- [Resume Processing Runs Table](/app/database/docs/sqlite/schemas/resume-processing-runs.md)
- [Persist Resume Processing Run Technical Process](/app/database/docs/system/database-adapter/processes/persist-resume-processing-run.md)
