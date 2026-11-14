# CLI Component Architecture Decision Log

This log indexes the component-level Architecture Decision Records (ADRs) for the CLI component. Entries are ordered with the newest decisions first.

| Date | Decision | Status |
| --- | --- | --- |
| 2026-11-14 | [Inject CLI dependencies explicitly](11-14-26/explicit-cli-dependencies.md) — Build the CLI with an injected `CLIDependencies` value, use a narrow resume-listing capability, and remove global dependency access and fallback resolution. | Accepted |
| 2026-11-07 | [Establish development application startup](11-07-26/development-startup-paths.md) — Place startup orchestration in the CLI, inject database initialization from a composition root, and use development-only data paths under `cli/data/`. | Accepted |
