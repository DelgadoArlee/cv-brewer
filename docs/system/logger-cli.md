# Logger CLI Process

## 1. Purpose / Summary

The logger CLI process starts a dedicated log-review interface, offers the available local log databases, prepares the selected source, and presents `llm`, `resume-upload`, `error`, and `all` views that generate HTML reports so reviewers can inspect stored LLM logs and resume processing logs in a web browser without exposing main application workflows.

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
    J -->|Yes| M[Present llm, resume-upload, error, all]
    M --> N{Option selected?}
    N -->|No selection| M
    N -->|llm| O[Query stored LLM logs]
    N -->|error| P[Query error records from both sources]
    N -->|all| Q[Query all records from both sources]
    N -->|resume-upload| R[Present view runs and view steps]
    R --> S{Child option selected?}
    S -->|No selection| R
    S -->|view runs| T[List processing runs and show details]
    S -->|view steps| U[List runs by run id and start date/time]
    U --> V{Run selected?}
    V -->|No| U
    V -->|Yes| W[Show selected run processing steps]
    O --> X{Query succeeded?}
    P --> X
    Q --> X
    T --> X
    W --> X
    X -->|No| Y[Report query failure]
    X -->|Yes| Z[Write HTML report, open browser, and print path]
    Y --> L
    Z --> L
````

## 3. Rules

- The process must discover available log databases before presenting the selection.
- The process must offer `dev`, `e2e`, and `test` in that order, and must offer only databases that exist.
- The process must default to `dev` when it is available, otherwise to the first available source.
- The process must skip the selection when exactly one database is available.
- The process must report an error and stop when no database is available.
- The process must initialize the selected database before querying logs.
- The process must receive its source capabilities and both LLM log and processing log query capabilities from the application composition root.
- The process must present exactly four log menu options: `llm`, `resume-upload`, `error`, and `all`.
- Selecting `llm` must query stored LLM activity log records, including the done reason when present, and generate an HTML report.
- Selecting `resume-upload` must present a child menu with exactly two options: `view runs` and `view steps`.
- Selecting `view runs` must generate an HTML report with processing-run-specific columns.
- Selecting `view steps` must list selectable processing runs labeled by run id and start date/time, then generate an HTML report for the selected run's processing step details.
- Selecting `error` must query error records from both LLM logs and processing runs. An LLM record is an error when its status is `FAILED` or `TIMEOUT`, or when its error type or error message is non-null. A processing run is an error when its status is `FAILED`, `VALIDATION_FAILED`, or `PARTIAL_SUCCESS`, or when its error object is non-null.
- Selecting `all` must query all records from both LLM logs and processing runs and generate one newest-first HTML report.
- Each view must return at most 100 rows. Query APIs must enforce the limit, and combined views must merge results before capping at the 100 newest records.
- The process must use LLM logs and processing runs only for `error` and `all`, and must expose processing steps only through `resume-upload > view steps`.
- LLM, processing run, and processing step reports must display duration in seconds. All HTML log reports must display stored CPU and memory performance values, including start, peak, and end memory, memory delta, average and peak CPU usage, and sample count.
- HTML reports must be written under `./logs/<source>/` with a full UTC creation timestamp and log type in the filename.
- After generating a report, the process must attempt to open it in the default browser and print the generated path. If the browser cannot be opened, the path must still be printed with a warning.
- The process must report startup and query failures clearly.
- The process must end after the selected view completes.

## 4. Constraints

- The logger CLI must not create a database that does not exist.
- The logger CLI must not invoke language models.
- The logger CLI must not access database implementations directly.
- The logger CLI must not import main application commands.
- The logger CLI must not expose resume upload, generation, or deletion workflows; `resume-upload` offers read-only processing log views only.
- The logger CLI must not modify stored log records or change database schemas.

## 5. References

- [Render Logger Reports as HTML](/docs/adr/Architecture/2026-11-20/html-log-reports.md)
- Log Report Fields: [LLM](/docs/log-reports/llm.md), [Processing Runs](/docs/log-reports/processing-runs.md), [Processing Steps](/docs/log-reports/processing-steps.md), [Error](/docs/log-reports/error.md), [All](/docs/log-reports/all.md)
- [Expand Logger CLI Log Views](/docs/adr/Architecture/2026-11-20/logger-cli-log-views.md)
- [LLM Activity Logging Feature Overview](/docs/features/llm-activity-logging.md)
- [Separate Logger CLI Entry Point Decision](/docs/adr/Architecture/2026-11-19/logger-cli-entry-point.md)
- [Log Source Selection Decision](/docs/adr/Architecture/2026-11-19/logger-log-source-selection.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Logger CLI Technical Process](/app/cli/docs/processes/logger-cli.md)
- [CLI Component Technical Specification](/app/cli/docs/technical-specification.md)
