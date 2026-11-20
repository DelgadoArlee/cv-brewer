# Query Processing Logs Process

## 1. Purpose / Summary

The query processing logs process retrieves stored resume processing run and step records through the Database Service for execution review. It supports listing all runs, listing a bounded set of the newest runs, listing a bounded set of the newest error-indicating runs, and listing the steps of one run with an optional cap, so reviewers can inspect recent or failed processing activity without accessing the database directly.

## 2. Process Flow

````mermaid
flowchart TD
    A([Start]) --> B{Requested query}
    B -->|All runs| C[Retrieve all processing runs]
    B -->|Recent runs with limit| D[Retrieve newest processing runs up to limit]
    B -->|Error runs with limit| E[Filter to error-indicating processing runs]
    E --> F[Retrieve newest matches up to limit]
    B -->|Steps for one run| G{Steps limited?}
    G -->|No| H[Retrieve steps in execution order]
    G -->|Yes| I[Retrieve newest started steps up to limit]
    C --> J{Query succeeded?}
    D --> J
    F --> J
    H --> J
    I --> J
    J -->|No| K[Report query failure]
    J -->|Yes| L([Return mapped run or step records])
    K --> M([Stop])
````

## 3. Rules

- **must** support listing all stored processing runs.
- **must** support listing a caller-limited number of the newest processing runs ordered by start time descending.
- **must** support listing a caller-limited number of the newest error-indicating processing runs ordered by start time descending.
- **must** treat a run as error-indicating when its status is `FAILED`, `VALIDATION_FAILED`, or `PARTIAL_SUCCESS`, or when an embedded error object is present.
- **must** support listing all steps belonging to one run, ordered by step order and attempt number.
- **must**, when a step limit is supplied, return the newest steps by start time up to that limit.
- **must** return mapped application-level records without exposing database-specific objects.
- **must** report query failures to the caller.

## 4. Constraints

- The process provides read-only access; it must not create, update, or delete processing run or step records.
- No schema or migration changes are introduced by this process.
- The process must not provide direct database access to the CLI; all queries must be reached through the Database Service.
- The process does not construct run or step records or control processing workflow behavior.

## 5. References

- [Database Service System Overview](/docs/system/database-service/overview.md)
- [Resume Processing System Overview](/docs/system/resume-processing/overview.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Error Data Model](/docs/data/error.md)
- [Query Processing Logs Technical Process](/app/database/docs/system/database-adapter/processes/query-processing-logs.md)
