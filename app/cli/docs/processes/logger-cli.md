# Logger CLI Technical Process

## 1. Purpose

Start the dedicated logger CLI, offer the available local log databases, prepare the selected source, and display stored LLM activity logs.

## 2. Objective

Provide a log-only entry point that selects an existing log database before reusing the main CLI layout and exposing no main application workflows.

## 3. Scope

- Resolve application startup paths for `dev`, `e2e`, and `test`.
- Keep only sources whose database file exists.
- Present the available sources, defaulting to `dev` when present.
- Initialize the selected source through an injected factory.
- Present one `llm` menu item using shared CLI presentation helpers.
- Query and display all LLM activity logs through an injected query capability, including the done reason when present.
- Display stored durations in seconds.

The process does not create missing databases, process resumes, invoke language models, or access database implementations directly.

## 4. Rules & Constraints

- The composition root must resolve source paths and inject an ordered mapping of available sources.
- The CLI must receive all capabilities from its composition root.
- The CLI must skip the source prompt when exactly one source is available.
- The CLI must report an error and stop when no source is available.
- The CLI must report a startup failure for the selected source and must not continue to the log menu.
- The CLI log menu must contain exactly one item named `llm`.
- Selecting `llm` must query all logs and display them, including the done reason when present.
- The log table must display duration in seconds.
- The CLI must end after displaying logs.
- The CLI must not import main application commands or resume capabilities.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B[Receive available log sources]
    B --> C{Sources available?}
    C -->|No| D[Report failure and stop]
    C -->|Yes| E{More than one source?}
    E -->|No| F[Use the only source]
    E -->|Yes| G[Present source selection defaulting to dev]
    G --> H[Use the selected source]
    F --> I[Prepare the selected source through its factory]
    H --> I
    I --> J{Preparation succeeded?}
    J -->|No| K[Report failure and stop]
    J -->|Yes| L[Render panel and llm item]
    L --> M{llm selected?}
    M -->|No| L
    M -->|Yes| N[Query all LLM logs]
    N --> O{Query succeeded?}
    O -->|No| P[Report failure]
    O -->|Yes| Q[Render log table]
    P --> R([Stop])
    Q --> R
````

### Steps

1. Resolve startup paths for the three environments and retain only those whose database file exists.
2. Start the logger CLI application with the ordered available sources.
3. Report an error and stop when no sources are available.
4. Use the only available source directly, or present the source selection defaulting to `dev`.
5. Prepare the selected source through its injected factory and report a startup failure if preparation fails.
6. Render the shared panel and the single `llm` menu item.
7. Query and display all stored LLM activity logs, including the done reason when present and duration in seconds.
8. End the session.

## 6. Modules

- `logger_main.py` — Root composition root that resolves environment paths, filters available sources, and injects source factories.
- `app/cli/logger_app.py` — Defines the logger CLI Typer application.
- `app/cli/modules/logger_context.py` — Defines logger environments, source factories, and injected logger CLI dependencies.
- `app/cli/commands/logger_menu.py` — Selects an available source and prepares its dependencies.
- `app/cli/ui/logger_sources.py` — Renders the source-selection panel and prompt.
- `app/cli/commands/llm_menu.py` — Renders the single-item log menu.
- `app/cli/commands/llm_logs.py` — Coordinates log queries.
- `app/cli/ui/llm_logs.py` — Renders log records.
- `app/cli/ui/selection.py` — Provides shared menu-selection helpers.

## 7. Testing

### 7.1 Test Level

Process level.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| LOGCLI-001 | Stored LLM logs exist. | `llm` is selected. | All logs are displayed. |
| LOGCLI-002 | No logs exist. | `llm` is selected. | An empty result is reported. |
| LOGCLI-003 | A query fails. | `llm` is selected. | An error is reported. |
| LOGCLI-004 | `dev`, `e2e`, and `test` databases exist. | The logger starts. | Sources are offered in that order with `dev` selected by default. |
| LOGCLI-005 | A non-default source is selected. | The logger continues. | Only the selected source is prepared and queried. |
| LOGCLI-006 | Exactly one source exists. | The logger starts. | The source is used without a selection prompt. |
| LOGCLI-007 | A selected source fails to prepare. | The logger continues. | A startup error is reported and logs are not displayed. |
| LOGCLI-008 | Only some environment databases exist. | Available sources are resolved. | Missing databases are excluded from the selection. |
| LOGCLI-009 | No environment database exists. | The logger starts. | An error is reported and the session stops. |
| LOGCLI-010 | A stored log includes a done reason. | `llm` is selected. | The done reason is displayed. |
| LOGCLI-011 | A stored log includes a duration. | `llm` is selected. | The duration is displayed in seconds. |

### 7.3 Test Coverage

Tests must verify source availability and ordering, selection delegation, query delegation, and output handling.

### 7.4 Test Organization

Tests reside under `tests/cli/commands/`.

### 7.5 Test Dependencies

Use test doubles for source factories and the log query capability.

### 7.6 Testing Rules Compliance

Tests verify observable CLI behavior without importing main application workflows.

## 8. References

- [Logger CLI Process](/docs/system/logger-cli.md)
- [CLI Component Technical Specification](/app/cli/docs/technical-specification.md)
- [Separate Logger CLI Entry Point](/app/cli/docs/adr/11-19-26/logger-cli-entry-point.md)
- [Select the Logger CLI Log Source](/app/cli/docs/adr/11-19-26/logger-log-source-selection.md)
