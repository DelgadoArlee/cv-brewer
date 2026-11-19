# Select the Log Database in the Logger CLI

## Date

2026-11-19

## Status

Accepted

## Category

architecture

## Context

The [separate logger CLI entry point](/docs/adr/Architecture/2026-11-19/logger-cli-entry-point.md) currently reads only the development database. LLM activity is recorded in the managed end-to-end environment under `/tests/e2e/data/`, and reviewers also need to inspect the managed test database under `/tests/data/` through the same read-only interface. The [manual dependency injection decision](/docs/adr/Architecture/2026-11-14/manual-dependency-injection.md) requires the CLI to receive capabilities from a composition root instead of constructing database access itself.

## Decision

- Offer `dev`, `e2e`, and `test` as log database sources in that order.
- Offer only sources whose database file exists.
- Default to the first available source and skip the selection when exactly one source is available.
- Report an error and stop when no source database exists.
- Resolve source paths in the logger CLI composition root and inject a factory that prepares startup paths and a log-query capability for the selected source.
- Keep the log-review menu, its single `llm` item, and its read-only behavior unchanged after selection.
- This refines the dependency and menu clauses of the [separate logger CLI entry point decision](/docs/adr/Architecture/2026-11-19/logger-cli-entry-point.md).

## Consequences

- Reviewers can inspect development and end-to-end logs without starting the main application, and can inspect the test database when it contains logs.
- The composition root owns environment path resolution and the availability check.
- The source-selection prompt precedes the log menu, which still contains one item.
- An environment whose database has not been generated cannot be selected until it exists.
