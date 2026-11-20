# Persist Resume Processing Run Process

## 1. Purpose / Summary

The persist resume processing run process stores a resume processing run record so the outcome, timing, summary, performance, referenced resume identifiers, and embedded error data of a processing execution can be reviewed later. It accepts a complete run record and delegates persistence to the configured database adapter.

## 2. Process Flow

````mermaid
flowchart TD
    A([Start]) --> B[Receive resume processing run record]
    B --> C[Validate run record is complete]
    C --> D{Valid?}
    D -->|No| E[Log persistence failure]
    D -->|Yes| F[Store run record]
    F --> G{Storage succeeded?}
    G -->|No| H[Log persistence failure]
    G -->|Yes| I([Run record stored])
````

## 3. Rules

- The system must store each accepted run record without changing its recorded values.
- The system must preserve `resume_id` and `matched_resume_id` as identifier references without creating database relationships to resume records.
- The system must preserve embedded `summary`, `performance`, and `error` data as part of the run record.
- The system must report persistence failures through standard logging and must not stop resume processing.
- The system must not create, update, or delete resume data as part of this process.

## 4. Constraints

- The process records processing execution data only; it does not validate resume content or control resume-processing workflow decisions.
- A stored run record may exist for outcomes that do not produce a saved parsed resume.
- Resume identifier references do not imply ownership or foreign-key relationships.

## 5. References

- [Database Service System Overview](/docs/system/database-service/overview.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Error Data Model](/docs/data/error.md)
- [Persist Resume Processing Run Technical Process](/app/database/docs/system/database-adapter/processes/persist-resume-processing-run.md)
