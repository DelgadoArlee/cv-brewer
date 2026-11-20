# Add a Separate Logger CLI Entry Point

## Date

2026-11-19

## Status

Superseded

## Category

architecture

## Context

Reviewing stored LLM activity must not require starting the main application or exposing main application workflows to log reviewers. The log viewer therefore needs its own executable entry point while preserving the familiar layout of the main CLI. The [log source selection decision](/docs/adr/Architecture/2026-11-19/logger-log-source-selection.md) refined the dependency and menu clauses below. This ADR is superseded by the [expanded logger CLI log views decision](/docs/adr/Architecture/2026-11-20/logger-cli-log-views.md), which replaces the original menu and capability clauses; the separate entry point remains in force.

## Decision

- Add a second executable entry point invoked with `./logger.sh`.
- Reuse the main CLI's Typer application pattern, Rich presentation, menu selection behavior, startup initialization, and explicit dependency injection.
- Expose a read-only interactive log menu; its current options are defined by the [expanded logger CLI log views decision](/docs/adr/Architecture/2026-11-20/logger-cli-log-views.md).
- Inject log-query capabilities from the composition root; the current capabilities are defined by the expanded log views decision.
- Do not include any main application functions, resume workflows, resume data capabilities, or LLM invocation in the logger CLI.
- The main CLI entry point and its behavior remain unchanged.

## Consequences

- Two entry points share CLI presentation helpers but have separate dependency containers and menus.
- The logger CLI has a narrower dependency surface than the main CLI.
- Packaging and documentation must describe both entry points.
- A second executable entry point extends the prior single-executable packaging decision without replacing it.
