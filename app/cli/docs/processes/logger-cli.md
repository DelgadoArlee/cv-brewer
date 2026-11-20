# Logger CLI Technical Process

## 1. Purpose

Start the dedicated logger CLI, offer the available local log databases, prepare the selected source, and generate HTML reports for LLM logs and resume processing logs through the `llm`, `resume-upload`, `error`, and `all` views.

## 2. Objective

Provide a log-only entry point that selects an existing log database before presenting a four-option menu that generates HTML reports for LLM activity, processing runs, processing steps, errors, and a combined newest-first overview without exposing main application workflows.

## 3. Scope

- Resolve application startup paths for `dev`, `e2e`, and `test`.
- Keep only sources whose database file exists.
- Present the available sources, defaulting to `dev` when present.
- Initialize the selected source through an injected factory.
- Present the `llm`, `resume-upload`, `error`, and `all` options using shared CLI presentation helpers.
- Present the `resume-upload` child options `view runs` and `view steps`.
- Query LLM activity logs, processing run details, and processing step details through injected query capabilities, including the done reason when present.
- Query error records from LLM logs and processing runs, and merge both sources into a single newest-first HTML report for `all`.
- Enforce the 100-row limit in query capabilities and cap merged views at the 100 newest records.
- Write escaped standalone HTML reports under `./logs/<source>/` with full UTC timestamp filenames.
- Attempt to open generated reports in the default browser and print the report path.
- Display stored durations in seconds in HTML reports.
- Display stored CPU and memory performance metrics in HTML reports: start, peak, and end memory, memory delta, average and peak CPU usage, and sample count.

The process does not create missing databases, process resumes, invoke language models, access database implementations directly, or change stored records and schemas.

## 4. Rules & Constraints

- The composition root must resolve source paths and inject an ordered mapping of available sources.
- The composition root must inject both LLM log and processing log query capabilities, the selected source, the report directory, and the browser-opening capability into the logger CLI.
- The CLI must receive all capabilities from its composition root and must not import database implementations.
- The CLI must skip the source prompt when exactly one source is available.
- The CLI must report an error and stop when no source is available.
- The CLI must report a startup failure for the selected source and must not continue to the log menu.
- The CLI log menu must contain exactly four items: `llm`, `resume-upload`, `error`, and `all`.
- Selecting `llm` must query stored LLM activity logs, including the done reason when present, and generate an HTML report.
- Selecting `resume-upload` must open a child menu with exactly `view runs` and `view steps`.
- `view runs` must generate an HTML report for processing runs using processing-run-specific columns.
- `view steps` must list selectable processing runs labeled by run id and start date/time and, after a run is selected, generate an HTML report for that run's processing step details.
- `error` must query error records from both LLM logs and processing runs. LLM errors are status `FAILED` or `TIMEOUT` or a non-null error type or error message. Processing run errors are status `FAILED`, `VALIDATION_FAILED`, or `PARTIAL_SUCCESS` or a non-null error object.
- `all` must query all records from both LLM logs and processing runs and generate one newest-first HTML report.
- Query capabilities must enforce a maximum of 100 rows, and merged views must merge before capping at the 100 newest records.
- LLM logs and processing runs must be used only by `error` and `all`; processing steps must be reachable only through `resume-upload > view steps`.
- LLM, processing run, and processing step reports must display duration in seconds.
- HTML log reports must display start memory, peak memory, end memory, memory delta, average CPU usage, peak CPU usage, and sample count from stored performance records.
- HTML reports must be written under `./logs/<source>/` and named with a full UTC creation timestamp and log type.
- The CLI must print the generated report path and attempt to open it in the default browser.
- If the browser cannot be opened, the CLI must print a warning and keep the generated path visible.
- The CLI must report query and report-write failures and end after the selected view completes.
- The CLI must not import main application commands, resume upload workflows, resume listing, or resume deletion.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B[Receive available log sources and query capabilities]
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
    J -->|Yes| L[Render panel and four log options]
    L --> M{Option selected?}
    M -->|No| L
    M -->|llm| N[Query LLM logs up to 100 rows]
    M -->|resume-upload| O[Render view runs and view steps]
    M -->|error| P[Query errors from both sources]
    M -->|all| Q[Query all records from both sources]
    O --> R{Child option selected?}
    R -->|No| O
    R -->|view runs| S[Query processing runs for report]
    R -->|view steps| T[Render selectable runs by id and start time]
    T --> U{Run selected?}
    U -->|No| T
    U -->|Yes| V[Query steps for the selected run]
    P --> W[Merge error records, keep 100 newest]
    Q --> X[Merge all records, keep 100 newest]
    N --> Y{Query succeeded?}
    S --> Y
    V --> Y
    W --> Y
    X --> Y
    Y -->|No| Z[Report failure]
    Y -->|Yes| AA[Write HTML report, open browser, and print path]
    Z --> AB([Stop])
    AA --> AB
````

### Steps

1. Resolve startup paths for the three environments and retain only those whose database file exists.
2. Start the logger CLI application with the ordered available sources and both injected query capabilities.
3. Report an error and stop when no sources are available.
4. Use the only available source directly, or present the source selection defaulting to `dev`.
5. Prepare the selected source through its injected factory and report a startup failure if preparation fails.
6. Render the shared panel and the `llm`, `resume-upload`, `error`, and `all` options.
7. Route `llm` to the LLM log query and prepare stored records, including the done reason when present and duration in seconds.
8. Route `resume-upload` to the child menu, then route `view runs` to processing run records or `view steps` to a run picker labeled by run id and start date/time followed by the selected run's step records.
9. Route `error` to the error predicate across both sources and `all` to a merged newest-first query across both sources.
10. Cap each result at 100 rows, write an HTML report with duration and CPU/memory performance columns under `./logs/<source>/`, attempt to open it, print its path, and end the session.

## 6. Modules

- `/logger_main.py` — Root composition root that resolves environment paths, filters available sources, and injects source factories, query capabilities, report output directory, and browser opener.
- `/app/cli/logger_app.py` — Defines the logger CLI Typer application.
- `/app/cli/modules/logger_context.py` — Defines logger environments, source factories, injected logger CLI dependencies, and the maximum row count.
- `/app/cli/modules/logger_records.py` — Normalizes LLM logs and processing runs for combined views.
- `/app/cli/commands/logger_menu.py` — Selects an available source and prepares its dependencies.
- `/app/cli/ui/logger_sources.py` — Renders the source-selection panel and prompt.
- `/app/cli/ui/logger_menus.py` — Renders the logger and resume-upload menu panels.
- `/app/cli/ui/html_reports.py` — Builds escaped HTML documents, writes report files, and coordinates browser opening.
- `/app/cli/commands/llm_menu.py` — Renders the four-option log menu and routes to the selected view.
- `/app/cli/commands/llm_logs.py` — Coordinates LLM log queries.
- `/app/cli/ui/llm_logs.py` — Defines LLM log report columns and rows.
- `/app/cli/ui/performance.py` — Provides shared CPU and memory performance columns and value formatting for HTML reports.
- `/app/cli/commands/resume_upload_menu.py` — Renders the `view runs` and `view steps` child menu.
- `/app/cli/commands/processing_runs.py` — Coordinates processing run queries and details for `view runs`.
- `/app/cli/commands/processing_steps.py` — Coordinates run selection and step queries for `view steps`.
- `/app/cli/commands/error_logs.py` — Coordinates error queries across LLM logs and processing runs.
- `/app/cli/commands/all_logs.py` — Coordinates the merged newest-first query across LLM logs and processing runs.
- `/app/cli/ui/log_overview.py` — Defines the shared newest-first overview report columns and rows.
- `/app/cli/ui/processing_runs.py` — Defines processing run report columns and rows.
- `/app/cli/ui/processing_steps.py` — Renders the run picker and defines processing step report columns and rows.
- `/app/cli/ui/selection.py` — Provides shared menu-selection helpers.

## 7. Testing

### 7.1 Test Level

Process level.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| LOGCLI-001 | Stored LLM logs exist. | `llm` is selected. | All logs appear in an HTML report. |
| LOGCLI-002 | No logs exist. | `llm` is selected. | An HTML report with an empty result is generated. |
| LOGCLI-003 | A query fails. | `llm` is selected. | An error is reported and no HTML report is generated. |
| LOGCLI-004 | `dev`, `e2e`, and `test` databases exist. | The logger starts. | Sources are offered in that order with `dev` selected by default. |
| LOGCLI-005 | A non-default source is selected. | The logger continues. | Only the selected source is prepared and queried. |
| LOGCLI-006 | Exactly one source exists. | The logger starts. | The source is used without a selection prompt. |
| LOGCLI-007 | A selected source fails to prepare. | The logger continues. | A startup error is reported and no report is generated. |
| LOGCLI-008 | Only some environment databases exist. | Available sources are resolved. | Missing databases are excluded from the selection. |
| LOGCLI-009 | No environment database exists. | The logger starts. | An error is reported and the session stops. |
| LOGCLI-010 | A stored log includes a done reason. | `llm` is selected. | The done reason appears in the HTML report. |
| LOGCLI-011 | A stored log includes a duration. | `llm` is selected. | The duration appears in seconds in the HTML report. |
| LOGCLI-012 | The logger menu is rendered. | Options are listed. | Exactly `llm`, `resume-upload`, `error`, and `all` are offered. |
| LOGCLI-013 | `resume-upload` is selected. | The child menu is rendered. | Exactly `view runs` and `view steps` are offered. |
| LOGCLI-014 | Processing run records exist. | `view runs` is selected. | Runs appear in an HTML report with their details. |
| LOGCLI-015 | Processing runs exist. | `view steps` is selected. | Runs are selectable and labeled by run id and start date/time. |
| LOGCLI-016 | A run is selected in `view steps`. | The run is opened. | That run's processing step details appear in an HTML report. |
| LOGCLI-017 | LLM logs and processing runs contain errors and non-errors. | `error` is selected. | Only records matching the agreed error predicate appear in the report. |
| LOGCLI-018 | LLM logs and processing runs exist. | `all` is selected. | Both record types appear in one newest-first HTML report. |
| LOGCLI-019 | More than 100 records exist in a view. | A view is queried. | At most 100 rows are written to the report. |
| LOGCLI-020 | More than 100 combined records exist. | `error` or `all` is selected. | Results are merged and capped at the 100 newest records. |
| LOGCLI-021 | Processing steps exist. | `llm`, `error`, or `all` is selected. | Processing steps are not included outside `view steps`. |
| LOGCLI-022 | Both query capabilities are injected. | Any view is opened. | Queries use the injected capabilities and no database implementation is imported. |
| LOGCLI-023 | Stored records include CPU and memory performance values. | An HTML report is generated. | The performance columns contain the stored values. |
| LOGCLI-024 | A data view is selected. | The HTML report is written. | The report is stored under `./logs/<source>/` with a timestamp and log-type filename. |
| LOGCLI-025 | A browser opener is injected. | A report is generated. | The opener receives the report file URI and the path is printed. |
| LOGCLI-026 | A browser opener reports failure. | A report is generated. | A warning is printed and the report path remains visible. |
| LOGCLI-027 | A report contains reserved HTML characters. | The report is generated. | Cell values are escaped in the HTML output. |

### 7.3 Test Coverage

Tests must verify source availability and ordering, menu and child-menu routing, run selection, error filtering, merge ordering, query delegation, row limits, HTML content, escaping, report filenames, per-source directories, browser-open behavior, path output, duration output, and performance output.

### 7.4 Test Organization

Tests reside under `tests/cli/commands/`.

### 7.5 Test Dependencies

Use test doubles for source factories and for both the LLM log and processing log query capabilities.

### 7.6 Testing Rules Compliance

Tests verify observable CLI behavior without importing main application workflows or database implementations.

## 8. References

- [Render Logger Reports as HTML](/docs/adr/Architecture/2026-11-20/html-log-reports.md)
- Log Report Fields: [LLM](/docs/log-reports/llm.md), [Processing Runs](/docs/log-reports/processing-runs.md), [Processing Steps](/docs/log-reports/processing-steps.md), [Error](/docs/log-reports/error.md), [All](/docs/log-reports/all.md)
- [Render Logger Data as HTML Reports](/app/cli/docs/adr/11-20-26/html-log-reports.md)
- [Expand Logger CLI Log Views](/docs/adr/Architecture/2026-11-20/logger-cli-log-views.md)
- [Implement Expanded Logger CLI Log Views](/app/cli/docs/adr/11-20-26/logger-cli-log-views.md)
- [Logger CLI Process](/docs/system/logger-cli.md)
- [CLI Component Technical Specification](/app/cli/docs/technical-specification.md)
- [Separate Logger CLI Entry Point](/app/cli/docs/adr/11-19-26/logger-cli-entry-point.md)
- [Select the Logger CLI Log Source](/app/cli/docs/adr/11-19-26/logger-log-source-selection.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
