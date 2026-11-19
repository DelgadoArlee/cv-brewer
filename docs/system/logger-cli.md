# Logger CLI Process

## 1. Purpose / Summary

The logger CLI process starts a dedicated log-review interface, offers the available local log databases, prepares the selected source, and presents a single `llm` option that lists stored LLM activity logs without exposing any main application workflows.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B[Discover available log databases]
    B --> C{Any database available?}
    C -->|No| D[Report no databases and stop]
    C -->|Yes| E{More than one available?}
    E -->|No| F[Use the only available database]
    E -->|Yes| G[Present database selection]
    G --> H[Use the selected database]
    F --> I[Initialize the selected database]
    H --> I
    I --> J{Initialization succeeded?}
    J -->|No| K[Report startup failure]
    K --> L([Stop])
    J -->|Yes| M[Present llm menu item]
    M --> N{Item selected?}
    N -->|No selection| M
    N -->|llm selected| O[Query stored LLM logs]
    O --> P{Query succeeded?}
    P -->|No| Q[Report query failure]
    P -->|Yes| R[Display all log records]
    Q --> L
    R --> L
````

## 3. Rules

- The process must discover available log databases before presenting the selection.
- The process must offer `dev`, `e2e`, and `test` in that order, and must offer only databases that exist.
- The process must default to `dev` when it is available, otherwise to the first available source.
- The process must skip the selection when exactly one database is available.
- The process must report an error and stop when no database is available.
- The process must initialize the selected database before querying logs.
- The process must receive its source capabilities from the application composition root.
- The process must present exactly one log menu item named `llm`.
- Selecting `llm` must query and display all stored LLM activity log records, including the done reason when present.
- The log table must display duration in seconds.
- The process must report startup and query failures clearly.
- The process must end after the `llm` item completes.

## 4. Constraints

- The logger CLI must not create a database that does not exist.
- The logger CLI must not invoke language models.
- The logger CLI must not access database implementations directly.
- The logger CLI must not import main application commands.
- The logger CLI must not expose resume data capabilities.

## 5. References

- [LLM Activity Logging Feature Overview](/docs/features/llm-activity-logging.md)
- [Separate Logger CLI Entry Point Decision](/docs/adr/Architecture/2026-11-19/logger-cli-entry-point.md)
- [Log Source Selection Decision](/docs/adr/Architecture/2026-11-19/logger-log-source-selection.md)
- [Logger CLI Technical Process](/app/cli/docs/processes/logger-cli.md)
- [CLI Component Technical Specification](/app/cli/docs/technical-specification.md)
