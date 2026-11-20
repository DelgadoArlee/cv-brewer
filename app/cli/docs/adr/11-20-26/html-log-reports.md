# Render Logger Data as HTML Reports

## Date

2026-11-20

## Status

Accepted

## Context

The [HTML log reports decision](/docs/adr/Architecture/2026-11-20/html-log-reports.md) replaces terminal table output for logger data views with generated HTML reports. Within the CLI component, the [expanded logger CLI log views decision](/app/cli/docs/adr/11-20-26/logger-cli-log-views.md) defined the current command routing and Rich presentation modules. The [explicit CLI dependencies decision](/app/cli/docs/adr/11-14-26/explicit-cli-dependencies.md) continues to require runtime capabilities to be injected from the composition root.

## Decision

- Add a shared CLI UI report module that builds standalone HTML documents with inline CSS using only the Python standard library.
- Escape every record value before placing it in HTML.
- Replace the Rich table bodies in the LLM, processing run, processing step, and overview UI modules with reusable HTML column and row definitions.
- Keep the existing column sets, including the duration and CPU/memory performance columns.
- Have data-view commands write an HTML report through an injected report directory and browser-opening capability.
- Store reports in `./logs/<source>/` with filenames matching `YYYY-MM-DDTHHMMSSffffffZ-<log-type>.html`.
- Use report types `llm`, `processing-runs`, `processing-steps-<run-id>`, `error`, and `all`.
- Print the report path after successful generation and warn when the browser opener reports failure.
- Keep query failures as CLI error messages without generating a report.
- Add `/scripts/clear-logs.sh` to delete `./logs` and add `/logs` to repository ignore rules.
- Keep the menu panels, source prompts, run picker, status messages, and error messages in the terminal.

## Consequences

- The [expanded logger CLI log views decision](/app/cli/docs/adr/11-20-26/logger-cli-log-views.md) is superseded for its Rich table presentation clauses; its menu, routing, query, and row-limit decisions remain in force.
- `LoggerCLIDependencies` carries the selected source, report directory, and browser-opening capability.
- Tests use temporary report directories and fake browser openers, and verify report files instead of terminal table rows.
- No new HTML or templating dependency is added to the application package.
- The cleanup script and generated report directory are documented in the repository structure.
