# Use Python and uv for the CVBrewer implementation

## Date

2026-11-04

## Status

Accepted

## Context

CVBrewer must bundle the CLI and Core into a single executable, run on Windows and macOS with Linux optional, process PDFs, validate JSON schemas, persist structured data, and communicate with a user-installed local LLM. The implementation language must support these capabilities without introducing unnecessary operational services. Python was selected by the developer.

## Decision

Use Python 3.12 as the implementation language and `uv` for dependency management, environment management, and lockfiles.

Maintain CVBrewer as a single Python distribution with internal packages for the CLI, Core, database, LLM, schemas, and templates. The components remain logically separate but are bundled into one executable.

Type hints are required, and the codebase is checked with ruff and mypy.

## Consequences

- Python provides mature libraries for PDF processing, schema validation, persistence, and local LLM communication.
- A single distribution keeps the build and packaging path simpler than maintaining separate deployable services.
- Component boundaries must be enforced through package structure, interfaces, and tests because the components share one distribution.
- The Python runtime and dependencies are bundled into the executable, increasing artifact size.
- Builds must run on each target operating system.
