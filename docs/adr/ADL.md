# Architecture Decision Log

This log indexes the Architecture Decision Records (ADRs) for CVBrewer. Entries are ordered with the newest decisions first.

| Date | Decision | Status |
| --- | --- | --- |
| 2026-11-13 | [Move the Database Service into the Core application layer](Architecture/2026-11-13/database-service-to-core.md) — Own application-level resume data operations in Core while Database retains adapters and implements Core-owned contracts. | Accepted |
| 2026-11-13 | [Adopt a single `app/` project with component modules](repositories/26-11-13/app-project-layout.md) — Group `cli`, `core`, `database`, and `llm` under `app/`, remove `<component>/src`, and package them as modules of one `cv-brewer` project. | Accepted |
| 2026-11-11 | [Use an LLM Service abstraction with pluggable LLM adapters](Architecture/2026-11-11/llm-service-abstraction.md) — Define application-level LLM operations behind an LLM Service that adapters implement; the Core constructs prompts and supplies JSON Schemas. | Accepted |
| 2026-11-04 | [Core owns file-type and PDF validation](Architecture/2026-11-04/validation-responsibilities.md) — The CLI discovers files and passes them to the Core; the Core performs all file-type and PDF validation. | Accepted |
| 2026-11-04 | [Use Typer and Rich for a hybrid CLI](Architecture/2026-11-04/cli-interface.md) — Provide direct subcommands plus an interactive menu, with the CLI limited to orchestration and file-byte handoff. | Accepted |
| 2026-11-04 | [Generate Markdown resumes for the MVP](Architecture/2026-11-04/markdown-output-mvp.md) — Render generated resumes as Markdown with Jinja2 and defer PDF rendering. | Accepted |
| 2026-11-04 | [Integrate local LLMs through a native Ollama adapter](Architecture/2026-11-04/llm-integration.md) — Communicate with the user's local Ollama service through the LLM Provider and Adapter boundaries. | Superseded |
| 2026-11-04 | [Use SQLite through SQLAlchemy and Alembic](Architecture/2026-11-04/database-persistence.md) — Use SQLite as the embedded default behind the Database Service and Adapter, with Alembic migrations. | Accepted |
| 2026-11-04 | [Use JSON Schema and Pydantic for data validation](Architecture/2026-11-04/schema-validation.md) — Use versioned JSON Schemas as the contract and Pydantic v2 for runtime models. | Accepted |
| 2026-11-04 | [Use pypdf and pdfplumber for PDF processing](Architecture/2026-11-04/pdf-processing.md) — Use pure-Python libraries for PDF validation, metadata, text extraction, and fingerprinting. | Accepted |
| 2026-11-04 | [Package CVBrewer as per-OS single executables with PyInstaller](Architecture/2026-11-04/cross-platform-packaging.md) — Build one-file executables per target OS, with macOS signing and notarization. | Accepted |
| 2026-11-04 | [Use Python and uv for the CVBrewer implementation](Architecture/2026-11-04/python-runtime-and-tooling.md) — Implement CVBrewer in Python 3.12 with uv and a single distribution containing internal component packages. | Accepted |
