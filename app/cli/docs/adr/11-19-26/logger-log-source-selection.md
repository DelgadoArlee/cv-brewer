# Select the Logger CLI Log Source

## Date

2026-11-19

## Status

Superseded

## Context

The [separate logger CLI entry point](/app/cli/docs/adr/11-19-26/logger-cli-entry-point.md) injects log query capabilities before the CLI starts. The [log source selection decision](/docs/adr/Architecture/2026-11-19/logger-log-source-selection.md) requires the logger CLI to choose among the available `dev`, `e2e`, and `test` databases while keeping database access outside the CLI component. This ADR is superseded by the [expanded logger CLI log views decision](/app/cli/docs/adr/11-20-26/logger-cli-log-views.md), which replaces the menu clause below while retaining source selection.

## Decision

- Define `LoggerEnvironment`, `LoggerDependenciesFactory`, and `LoggerSources` in `app/cli/modules/logger_context.py`.
- Map the environments to their data directories in `logger_main.py` and include only environments whose database file exists.
- Inject the ordered available sources into `create_logger_app` instead of a single dependency value.
- Add a shared source-selection presentation module under `app/cli/ui/` and a coordinating module under `app/cli/commands/`.
- Add an optional default index to the shared `select_option` helper so the source prompt can default to the first available source without changing the main CLI.
- Skip the source prompt when one source is available, report a startup failure for the selected source, and stop when none are available.
- Proceed to the log menu defined by the [expanded logger CLI log views decision](/app/cli/docs/adr/11-20-26/logger-cli-log-views.md) after the selected source is prepared.

## Consequences

- The CLI never resolves database paths or constructs repositories.
- The source prompt and the log menu are separate presentation steps.
- The shared selection helper gains a parameter but keeps its existing behavior for the main CLI.
- Logger process tests supply source mappings through test doubles instead of patching module globals.
