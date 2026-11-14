# Inject CLI Dependencies Explicitly

## Date

2026-11-14

## Status

Accepted

## Context

The CLI application used module-level globals for startup paths and the resume processor. It also exposed `configure_application`, `get_startup_paths`, and `get_resume_processor` accessors, and could construct database and LLM services lazily inside the CLI. Menu and Options commands resolved dependencies through fallback paths, and the Options menu read `ResumeProcessor._resume_service` directly.

These patterns obscured required dependencies, duplicated composition, and made CLI behavior depend on mutable global state.

## Decision

- Define `CLIDependencies` and `ResumeLister` in `app/cli/modules/context.py`.
- Build the Typer application through `create_app(dependencies)`.
- Store the injected dependencies in the Typer context and read them from command callbacks.
- Require explicit startup paths and a resume processor for Resume Upload.
- Provide imported-resume listing through the injected `ResumeLister` capability.
- Remove `configure_application`, `get_startup_paths`, `get_resume_processor`, module-level dependency globals, fallback dependency resolution, and unused compatibility aliases.

This implements the application-level decision in [Use Manual Dependency Injection with a Single Composition Root](../../../../../docs/adr/Architecture/2026-11-14/manual-dependency-injection.md).

## Consequences

- The CLI application is created with all runtime dependencies already wired.
- Direct commands and the interactive menu use the same injected dependencies.
- The Options menu no longer accesses resume processor internals.
- CLI process tests construct dependencies explicitly instead of patching module globals.
- The CLI remains free of database and LLM implementation imports.
