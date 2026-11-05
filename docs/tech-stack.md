# CVBrewer Tech Stack

## 1. Purpose

This document summarizes the technology stack selected for CVBrewer. It is a reference for the project's high-level technology choices and links to the Architecture Decision Records (ADRs) that established them.

This document does not replace the ADRs, requirements, architecture, or system documentation.

## 2. Stack Summary

| Area                | Technology                                              | Purpose                                                      |
| ------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| Language            | Python 3.12                                             | Implementation language for the CLI and Core                 |
| Tooling             | `uv`                                                    | Dependency management, environments, and lockfiles           |
| CLI                 | Typer + Rich                                            | Commands, interactive menu, prompts, progress, and tables    |
| PDF validation      | `pypdf`                                                 | Signature, encryption, structure, and metadata checks        |
| PDF text extraction | `pdfplumber` / `pdfminer.six`                           | Readable-content checks and text extraction                  |
| Schema validation   | JSON Schema 2020-12 + Pydantic v2 + `jsonschema`        | Data contracts, runtime models, and deterministic validation |
| Persistence         | SQLite + SQLAlchemy 2.0 + Alembic                       | Embedded database, adapter boundary, and migrations          |
| LLM integration     | LLM Adapter → User's chosen LLM service                 | Communication with the user's selected external LLM service |
| Rendering           | Jinja2 → Markdown                                       | Generated resume output for the MVP                          |
| Packaging           | PyInstaller                                             | Per-OS single executables                                    |
| Quality             | pytest, ruff, mypy, pre-commit                          | Testing, linting, formatting, and type checking              |
| Platforms           | Windows and macOS required; Linux optional              | Supported operating systems                                  |
| Data locations      | Windows Documents; macOS Application Support; Linux XDG | Input and output folder locations                            |

## 3. Component Mapping

| Component              | Technology responsibility                                                                                |
| ---------------------- | -------------------------------------------------------------------------------------------------------- |
| CLI                    | User interaction, folder management, file discovery, workflow coordination, and result reporting         |
| Core Processing Engine | File-type checks, PDF validation, text extraction, parsing, schema validation, generation, and rendering |
| Database Service       | Application-level data operations                                                                        |
| Database Adapter       | SQLite access through SQLAlchemy and Alembic                                                             |
| LLM Adapter            | Communication with the user's chosen LLM service                                                         |

## 4. Boundaries

- The CLI is orchestration-only. It discovers files, reads file bytes, passes immutable payloads to the Core, and reports outcomes.
- The Core owns all file-type and PDF validation. The CLI does not filter files by type.
- The Core does not access the file system directly; it operates on the bytes supplied by the CLI.
- The Core depends on the Database Service interface, not on SQLAlchemy or SQLite directly.
- The Core depends on the LLM Adapter interface, not on any specific LLM implementation.
- JSON Schema is the data contract; validation occurs before storage, generation, and rendering.
- Generated resume data is not stored in the database. Generated output is saved as a Markdown file in the output folder.
- PDF rendering is deferred. The renderer boundary allows PDF support to be added later.

## 5. Platform and Packaging

- Windows and macOS are required for the first release. Linux is optional.
- PyInstaller produces one-file executables per target operating system.
- Builds run on their target operating system; PyInstaller does not cross-compile.
- macOS artifacts are code-signed and notarized. Windows signing is optional.
- The Python runtime and dependencies are bundled into each executable.
- Input and output folders follow the operating system conventions documented in the input folder initialization process.

## 6. Development and Verification

- Dependencies and environments are managed with `uv`.
- Tests use pytest.
- Linting and formatting use ruff.
- Type checking uses mypy.
- Pre-commit runs the local quality checks before commits.
- CI builds and verifies the Windows and macOS artifacts. Linux is optional.

## 7. Decisions

| Decision                                           | ADR                                                                          |
| -------------------------------------------------- | ---------------------------------------------------------------------------- |
| Use Python and `uv`                                | [Python runtime and tooling](adr/2026-11-04/python-runtime-and-tooling.md)   |
| Package per-OS single executables with PyInstaller | [Cross-platform packaging](adr/2026-11-04/cross-platform-packaging.md)       |
| Use `pypdf` and `pdfplumber` for PDF processing    | [PDF processing](adr/2026-11-04/pdf-processing.md)                           |
| Use JSON Schema and Pydantic for validation        | [Schema validation](adr/2026-11-04/schema-validation.md)                     |
| Use SQLite through SQLAlchemy and Alembic          | [Database persistence](adr/2026-11-04/database-persistence.md)               |
| Integrate LLMs through an adapter pattern           | [LLM integration](adr/2026-11-04/llm-integration.md)                         |
| Generate Markdown resumes for the MVP              | [Markdown output MVP](adr/2026-11-04/markdown-output-mvp.md)                 |
| Use Typer and Rich for a hybrid CLI                | [CLI interface](adr/2026-11-04/cli-interface.md)                             |
| Core owns file-type and PDF validation             | [Validation responsibilities](adr/2026-11-04/validation-responsibilities.md) |

## 8. References

- [System Architecture](architecture.md)
- [Requirements](requirements.md)
- [General System Rules](system-rules.md)
- [Architecture Decision Log](adr/ADL.md)
