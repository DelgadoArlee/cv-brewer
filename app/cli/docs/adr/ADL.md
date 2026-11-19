# CLI Component Architecture Decision Log

This log indexes the component-level Architecture Decision Records (ADRs) for the CLI component. Entries are ordered with the newest decisions first.

| Date | Decision | Status | High-Level ADR |
| --- | --- | --- | --- |
| 2026-11-19 | [Select the logger CLI log source](/app/cli/docs/adr/11-19-26/logger-log-source-selection.md) — Offer available `dev`, `e2e`, and `test` sources through an injected source mapping before the single-item `llm` menu. | Accepted | [Select the Log Database in the Logger CLI](/docs/adr/Architecture/2026-11-19/logger-log-source-selection.md) |
| 2026-11-19 | [Separate Logger CLI entry point](/app/cli/docs/adr/11-19-26/logger-cli-entry-point.md) — Add `logger.sh` with an injected log-query capability, a single `llm` menu item, and no main application functions. | Superseded | [Separate Logger CLI Entry Point](/docs/adr/Architecture/2026-11-19/logger-cli-entry-point.md) |
| 2026-11-14 | [Inject CLI dependencies explicitly](/app/cli/docs/adr/11-14-26/explicit-cli-dependencies.md) — Build the CLI with an injected `CLIDependencies` value, use a narrow resume-listing capability, and remove global dependency access and fallback resolution. | Accepted | [Manual Dependency Injection](/docs/adr/Architecture/2026-11-14/manual-dependency-injection.md) |
| 2026-11-07 | [Establish development application startup](/app/cli/docs/adr/11-07-26/development-startup-paths.md) — Place startup orchestration in the CLI, inject database initialization from a composition root, and use development-only data paths under `cli/data/`. | Accepted | — |
