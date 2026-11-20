# Expand Logger CLI Log Views

## Date

2026-11-20

## Status

Superseded

## Category

architecture

## Context

The [separate logger CLI entry point](/docs/adr/Architecture/2026-11-19/logger-cli-entry-point.md) established a read-only log-review interface with a single `llm` item, and the [log database selection decision](/docs/adr/Architecture/2026-11-19/logger-log-source-selection.md) added selection among the available `dev`, `e2e`, and `test` sources. Resume processing runs and steps are now persisted as their own audit records, as decided in [Add resume processing run and step logging](/docs/adr/Architecture/2026-11-19/resume-processing-run-logging.md). Reviewers need to inspect those records, isolate errors across both log families, and review all records together without leaving the read-only entry point. The [manual dependency injection decision](/docs/adr/Architecture/2026-11-14/manual-dependency-injection.md) continues to require capabilities to be supplied by a composition root rather than constructed inside the CLI.

## Decision

- Replace the single-item logger menu with exactly four options: `llm`, `resume-upload`, `error`, and `all`.
- Give `resume-upload` a child menu with exactly two options: `view runs` and `view steps`.
- Make `view runs` list and show details for processing run records in the same manner as LLM logs.
- Make `view steps` list selectable processing runs labeled by run id and start date/time, then show the selected run's processing step details in a table in the same manner as LLM logs.
- Make `error` query all error records from both LLM logs and processing runs. An LLM record is an error when its status is `FAILED` or `TIMEOUT`, or when its error type or error message is non-null. A processing run is an error when its status is `FAILED`, `VALIDATION_FAILED`, or `PARTIAL_SUCCESS`, or when its error object is non-null.
- Make `all` query all records from both LLM logs and processing runs and display them in one newest-first table.
- Limit every view to 100 rows. Query APIs enforce the limit, and combined views merge results before capping at the 100 newest records.
- Use LLM logs and processing runs only for `error` and `all`. Keep processing steps only under `resume-upload > view steps`.
- Keep the existing source selection and read-only character of the logger CLI; this decision replaces the menu and capability clauses of the earlier logger CLI decisions while carrying their source-selection behavior forward.
- Provide processing log and LLM log query capabilities to the CLI from the composition root. The CLI must not access database implementations directly.
- Make no database schema changes.

## Consequences

- Reviewers can inspect LLM logs, processing runs, processing steps, errors, and a combined newest-first view from one read-only entry point.
- The composition root must supply both LLM log and processing log query capabilities for the selected source.
- The CLI needs separate coordination and presentation modules for the expanded menu, child menu, combined views, and processing records.
- Earlier logger ADRs that fixed a single-item menu are superseded; source selection remains in force through this decision.
- No migration or data model work is required; row limits are enforced by query APIs and by the CLI when it merges combined results.
- The [HTML log reports decision](/docs/adr/Architecture/2026-11-20/html-log-reports.md) supersedes the table-output clauses of this decision; the menu, child menu, query, error-predicate, row-limit, source-selection, and read-only clauses remain in force.
