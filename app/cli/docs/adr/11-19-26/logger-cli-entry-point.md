# Separate Logger CLI Entry Point

## Date

2026-11-19

## Status

Superseded

## Context

The [separate logger CLI entry point](/docs/adr/Architecture/2026-11-19/logger-cli-entry-point.md) decision requires a second executable that looks like the main CLI but exposes only log querying. The [explicit CLI dependencies](/app/cli/docs/adr/11-14-26/explicit-cli-dependencies.md) decision requires dependencies to be injected rather than resolved inside the CLI. The [log source selection decision](/app/cli/docs/adr/11-19-26/logger-log-source-selection.md) refined the injected dependency and menu clauses below. This ADR is superseded by the [expanded logger CLI log views decision](/app/cli/docs/adr/11-20-26/logger-cli-log-views.md), which replaces the original menu and capability clauses; the separate entry point remains in force.

## Decision

- Add `logger.sh` and a root composition root for the logger CLI.
- Add a separate Typer application factory and dependency container in `app/cli/`.
- Share menu-selection presentation helpers with the main CLI rather than duplicating them.
- Present a read-only log menu whose current options are defined by the [expanded logger CLI log views decision](/app/cli/docs/adr/11-20-26/logger-cli-log-views.md).
- Inject log query capabilities and startup paths from the composition root.
- Do not import or call resume processing, resume listing, resume deletion, or LLM invocation in the logger CLI path.

## Consequences

- The logger CLI has no main application functions and a smaller dependency surface.
- The main CLI's menu and commands are not exposed through the logger CLI.
- Shared presentation changes affect both entry points and must preserve main CLI behavior.
