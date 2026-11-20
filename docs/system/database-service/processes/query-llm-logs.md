# Query LLM Logs Process

## 1. Purpose / Summary

The query LLM logs process retrieves stored LLM activity log records through the Database Service for review. It supports listing all records, listing a bounded set of the newest records, and listing a bounded set of the newest records that indicate an error, so reviewers can inspect recent or failed language-model activity without accessing the database directly.

## 2. Process Flow

````mermaid
flowchart TD
    A([Start]) --> B{Requested query}
    B -->|All logs| C[Retrieve all stored LLM logs]
    B -->|Recent logs with limit| D[Retrieve newest LLM logs up to limit]
    B -->|Error logs with limit| E[Filter to error-indicating LLM logs]
    E --> F[Retrieve newest matches up to limit]
    C --> G{Query succeeded?}
    D --> G
    F --> G
    G -->|No| H[Report query failure]
    G -->|Yes| I([Return mapped log records])
    H --> J([Stop])
````

## 3. Rules

- **must** support listing all stored LLM activity logs.
- **must** support listing a caller-limited number of the newest LLM activity logs ordered by creation time descending.
- **must** support listing a caller-limited number of the newest error-indicating LLM activity logs ordered by creation time descending.
- **must** treat a log as error-indicating when its status is `FAILED` or `TIMEOUT`, or when it carries an error type or an error message.
- **must** return mapped application-level records without exposing database-specific objects.
- **must** return an empty result when no records match the requested query.
- **must** report query failures to the caller.

## 4. Constraints

- The process provides read-only access; it must not create, update, or delete log records.
- No schema or migration changes are introduced by this process.
- The process must not provide direct database access to the CLI; all queries must be reached through the Database Service.
- The process does not build, interpret, or display log records.

## 5. References

- [LLM Activity Logging Feature Overview](/docs/features/llm-activity-logging.md)
- [Database Service System Overview](/docs/system/database-service/overview.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)
- [Query LLM Logs Technical Process](/app/database/docs/system/database-adapter/processes/query-llm-logs.md)
