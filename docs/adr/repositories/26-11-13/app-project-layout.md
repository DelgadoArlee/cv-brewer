# Adopt a Single `app/` Project with Component Modules

## Date

2026-11-13

## Status

Accepted

## Category

repositories

## Context

CVBrewer previously maintained each component (`cli`, `core`, `database`, `llm`) as a separate uv project at the repository root, with source code nested under `<component>/src/<component>/`.

The repository now groups application components under `app/`. The build backend (`uv_build`) rejects a module root outside the project, so `app/cli` cannot itself be packaged while each component remains an independent uv project. The project needed a layout that supports the new `app/` structure while keeping component boundaries clear and imports stable.

## Decision

Adopt a single uv project at `app/` containing the `cli`, `core`, `database`, and `llm` modules:

- Each component becomes a top-level module under `app/`, with its package files directly under `app/<component>/`.
- The `<component>/src` directories are removed.
- The `app/` project is named `cv-brewer` and packages all component modules.
- The root project becomes a workspace named `cv-brewer-workspace` that depends on `cv-brewer`.
- Component import names remain unchanged (`from cli...`, `from core...`, `from database...`, `from llm...`).
- Component documentation remains under `app/<component>/docs/`.
- The component summary and repository structure are documented in `app/README.md`.

## Consequences

- The application builds and installs as one distribution, matching the existing single-executable packaging approach.
- Component modules share one dependency set and one build configuration.
- Repository structure changes require updates to documentation, relative links, and source-path references.
- Component boundaries are preserved by module directories and documentation rather than separate projects.
