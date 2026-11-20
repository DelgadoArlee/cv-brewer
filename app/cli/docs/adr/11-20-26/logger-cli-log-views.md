# Implement Expanded Logger CLI Log Views

## Date

2026-11-20

## Status

Superseded

## Context

The [expanded logger CLI log views decision](/docs/adr/Architecture/2026-11-20/logger-cli-log-views.md) replaces the single `llm` menu item with a four-item menu and adds a `resume-upload` child menu. In the CLI component, the [separate logger CLI entry point](/app/cli/docs/adr/11-19-26/logger-cli-entry-point.md) fixed the original menu shape, and the [logger CLI log source selection](/app/cli/docs/adr/11-19-26/logger-log-source-selection.md) decision established source selection through an injected source mapping. The [explicit CLI dependencies decision](/app/cli/docs/adr/11-14-26/explicit-cli-dependencies.md) requires all capabilities to be injected rather than resolved in the CLI.

## Decision

- Present the logger menu with exactly `llm`, `resume-upload`, `error`, and `all`, and route each option to a dedicated command module.
- Add `/app/cli/commands/resume_upload_menu.py` to present the `resume-upload` child menu with exactly `view runs` and `view steps`.
- Add `/app/cli/commands/processing_runs.py` to coordinate `view runs`, and `/app/cli/commands/processing_steps.py` to coordinate run selection and `view steps`.
- Add `/app/cli/commands/error_logs.py` to coordinate the error view and `/app/cli/commands/all_logs.py` to coordinate the combined view.
- Add `/app/cli/ui/log_overview.py` for the shared newest-first overview table, and `/app/cli/ui/processing_runs.py` and `/app/cli/ui/processing_steps.py` for processing record tables.
- Add `/app/cli/ui/logger_menus.py` for shared menu panels and `/app/cli/modules/logger_records.py` to normalize LLM logs and processing runs into combined-view records.
- Keep `/app/cli/commands/llm_menu.py` as the four-option logger menu coordinator and router; keep `/app/cli/commands/llm_logs.py` and `/app/cli/ui/llm_logs.py` for LLM log queries and presentation, and preserve the shared selection helpers.
- Receive LLM log and processing log query capabilities through `/app/cli/modules/logger_context.py` from the composition root; the CLI does not import database implementations.
- Apply the agreed row limit of 100 in the query capabilities. For `error` and `all`, merge LLM log and processing run results first, then cap the combined result at the 100 newest records.
- Use the agreed error predicate in the error view: LLM status `FAILED` or `TIMEOUT` or a non-null error type or error message, and processing run status `FAILED`, `VALIDATION_FAILED`, or `PARTIAL_SUCCESS` or a non-null error object.
- Label selectable processing runs by run id and start date/time in `view steps`, and show step details for the selected run in a table.
- Do not change database schemas or expose processing steps outside the `resume-upload > view steps` path.

## Consequences

- Logger command and UI modules are grouped by view instead of extending the single-item menu coordinator.
- The composition root and logger dependency container carry two query capabilities for the selected source.
- Tests supply both query capabilities through test doubles and verify menu routing, merging, error filtering, ordering, and the 100-row cap.
- The previous logger entry point and source selection ADRs no longer define the menu; source selection behavior remains in force through the high-level decision.
- The [HTML log reports decision](/app/cli/docs/adr/11-20-26/html-log-reports.md) supersedes the Rich table presentation clauses of this decision; the menu, routing, query, and row-limit clauses remain in force.
