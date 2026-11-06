# Command-Line Interface (CLI) Component Technical Specification

## 1. Purpose

This document defines the technical organization of the CLI component within CVBrewer. It describes how the CLI is structured and bounded so it can handle user interaction, local file management, and workflow coordination without coupling to Core processing, database, or LLM implementation details.

## 2. Objective

- Provide the user-facing interface for CVBrewer.
- Provide direct subcommands and an interactive menu when no command is supplied.
- Discover and check the designated input and output folders.
- Create and manage the input and output folders according to the application's folder-management rules.
- Discover files in the input folder and supply their content to the Core Processing Engine.
- Coordinate resume upload, generation, and deletion workflows with the Core.
- Save generated resume Markdown files in the designated output folder.
- Report workflow outcomes and errors to the user.
- Support non-interactive flags for automation.
- Remain part of the single executable used by the application.

## 3. Scope

### In Scope

- The CLI component package and its internal subpackages.
- User interaction, prompts, menus, progress reporting, tables, and error output.
- Input and output folder management and file discovery.
- Reading file bytes and passing immutable file payloads to the Core.
- Workflow coordination with the Core for resume upload, generation, and deletion.
- Saving generated Markdown files in the output folder.
- Non-interactive flags for automation.
- Component technical documentation.

### Out of Scope

- File-type signature verification, PDF validation, and readable-content checks.
- PDF text extraction, resume parsing, and schema validation.
- Resume generation and Markdown rendering.
- Database access, connections, queries, and transactions.
- LLM service communication.
- Core processing logic and validation rules.
- Modification or deletion of uploaded files in the input folder.
- Data model and schema definitions.
- System and module technical documentation.
- Implementation code and test cases.

## 4. Rules & Constraints

- The CLI must be orchestration-only and must coordinate work through the Core Processing Engine.
- The CLI must not perform file-type validation and must not filter discovered files by type.
- The CLI must not duplicate Core validation or processing logic.
- The CLI must read file bytes and pass immutable file payloads to the Core.
- The CLI must not access the Database Service, Database Adapter, or database implementation directly.
- The CLI must not access an LLM service directly.
- The CLI must not modify or delete uploaded files in the input folder as part of the upload workflow.
- The CLI must leave the acquisition and removal of uploaded files in the input folder to the user.
- The CLI must save generated Markdown files in the designated output folder.
- Destructive actions require explicit confirmation.
- The CLI must support non-interactive flags for automation.
- The interactive menu and direct subcommands must remain behaviorally consistent.
- The CLI must use Typer for command definitions and Rich for prompts, tables, progress, and error output.
- Input and output folder locations must follow the operating system conventions documented for the application.
- The CLI must not be independently deployable and must remain part of the combined CLI/Core executable.

## 5. Architectural & Design Approaches

### 5.1. Hybrid Command and Interactive Interface

- **Name:** Hybrid command and interactive interface.
- **Description:** The CLI supports both direct commands and a menu-driven interaction model.
- **Application:** Typer defines the direct subcommands, Rich provides prompts and output formatting, and the interactive menu is presented when the CLI is run without a command.

### 5.2. Orchestration-Only Boundary

- **Name:** Orchestration-only boundary.
- **Description:** The CLI coordinates workflows and delegates processing responsibilities to other components.
- **Application:** The CLI discovers files, reads bytes, passes payloads to the Core, and reports outcomes without performing validation, parsing, database access, LLM access, or rendering.

### 5.3. Byte-Oriented Handoff

- **Name:** Byte-oriented handoff.
- **Description:** File-system access is separated from content processing.
- **Application:** The CLI discovers files and supplies their bytes as immutable payloads to the Core, which performs file-type and PDF validation on the supplied content.

### 5.4. Single-Project Internal Packaging

- **Name:** Single-project internal packaging.
- **Description:** The CLI is maintained as one Python project containing internal packages.
- **Application:** The CLI package is organized under `cli/src/cli/` within the single application distribution.

## 6. Systems

| System | Description | Specification |
| --- | --- | --- |
| None documented | No CLI systems have been documented yet. | Not yet documented |

## 7. File Structure

````text
cli/
├── pyproject.toml          Project configuration and package metadata.
├── README.md               Package README file.
├── .python-version         Python version selection.
├── docs/
│   └── technical-specification.md
└── src/
    └── cli/
        └── __init__.py
````

## 8. Deployment

- The CLI is included in the combined CLI/Core executable and is not independently deployable.
- The Python runtime and dependencies are bundled into per-OS executables built with PyInstaller.
- Builds run on their target operating system because PyInstaller does not cross-compile.
- The CLI manages access to the local file system within the input and output folders.

## 9. References

- [System Architecture](../../docs/architecture.md)
- [Repository Architecture](../../docs/repository/architecture.md)
- [Tech Stack](../../docs/tech-stack.md)
- [Requirements](../../docs/requirements.md)
- [General System Rules](../../docs/system-rules.md)
- [Resume Upload System Overview](../../docs/system/resume-upload/overview.md)
- [Resume Generation System Overview](../../docs/system/resume-generation/overview.md)
- [Delete Resumes System Overview](../../docs/system/delete-resumes/overview.md)
- [Use Typer and Rich for a hybrid CLI](../../docs/adr/Architecture/2026-11-04/cli-interface.md)
- [Use Python and uv for the CVBrewer implementation](../../docs/adr/Architecture/2026-11-04/python-runtime-and-tooling.md)
- [Package CVBrewer as per-OS single executables with PyInstaller](../../docs/adr/Architecture/2026-11-04/cross-platform-packaging.md)
