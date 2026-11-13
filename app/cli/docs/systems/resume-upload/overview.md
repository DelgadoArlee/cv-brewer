# Resume Upload Technical System Specification

## 1. Purpose

Defines the CLI system that coordinates resume upload. The system prepares the input folder, discovers files, supplies their bytes to the Core Processing Engine, and reports per-file outcomes to the user.

## 2. Objective

- Ensure the resume input folder exists and is accessible.
- Discover every file in the input folder without filtering by type.
- Read file bytes and create immutable resume inputs for the Core.
- Process files independently and continue after individual failures.
- Report per-file processing stages while files are processed.
- Display a result table with stored, duplicate, and failed counts.

## 3. Scope

### In Scope

- Input folder creation and accessibility checks under `app/cli/commands/resume_upload.py`.
- File discovery, ordering, and byte reading.
- `ResumeInput` creation and delegation to the Core Processing Engine.
- Stage progress reporting and result rendering under `app/cli/ui/resume_upload.py`.
- Upload errors for inaccessible folders, unreadable files, and missing processors.

### Out of Scope

- File-type, PDF, parsing, and schema validation.
- Deduplication, metadata extraction, and storage.
- Database and LLM access.
- Deleting, renaming, or moving input files.
- Resume generation and deletion workflows.

## 4. Rules & Constraints

- Use the input folder from the CLI startup paths.
- Create the input folder with parent directories when it does not exist.
- Reject an input path that is not a directory.
- Discover regular files only and order them by file name.
- Do not filter discovered files by extension or type.
- Read file bytes in the CLI and pass them to the Core as `ResumeInput`.
- Process each file independently and continue after per-file failures.
- Report file read failures as processing-failure outcomes.
- Report an empty input folder as a normal completion outcome without processing files.
- Require a resume processor only when files are present.
- Report the current Core processing stage when a console is available.
- Display the result table after processing completes.
- Do not access the Database Service, Database Adapter, or LLM service directly.
- Do not modify or delete uploaded files.

## 5. Process

| Process | Description | Specification |
| --- | --- | --- |
| Resume Upload | Prepares the input folder, discovers files, delegates processing, and reports outcomes. | [Resume Upload Process](processes/resume-upload.md) |

## 6. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `StartupPaths` | CLI module | Provides the resume input folder location. |
| `ResumeProcessor` | Core interface | Processes resume inputs and reports outcomes. |
| `ResumeInput` | Core model | Carries file bytes and metadata to the Core. |
| `ResumeProcessingOutcome` | Core model | Describes the result for each processed file. |
| `ResumeProcessingStatus` | Core model | Classifies processing outcomes for display. |
| `rich` | External library | Provides progress display, tables, and console output. |

## 7. Test Cases

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| RU-SYS-001 | An input folder containing valid files. | Resume upload runs. | Each file is processed and outcomes are returned. |
| RU-SYS-002 | An input folder that does not exist. | Resume upload runs. | The folder is created before discovery. |
| RU-SYS-003 | An empty input folder. | Resume upload runs. | The upload completes normally and an empty-folder message is displayed. |
| RU-SYS-004 | A file that cannot be read. | Resume upload runs. | A processing-failure outcome is returned for that file. |
| RU-SYS-005 | Multiple files where one fails processing. | Resume upload runs. | Remaining files continue and each returns an outcome. |
| RU-SYS-006 | A console and a processing Core. | Resume upload runs. | Stage descriptions are reported and a result table is displayed. |

## 8. Diagrams

````mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Core
    User->>CLI: Select Import Resumes
    CLI->>CLI: Ensure input folder
    CLI->>CLI: Discover and read files
    loop Each file
        CLI->>Core: Process ResumeInput
        Core-->>CLI: Stage notification
        Core-->>CLI: ResumeProcessingOutcome
    end
    CLI-->>User: Display result table
````

## 9. Architecture Decision Log

| ADR | Decision Summary |
| --- | --- |
| [Use Typer and Rich for a hybrid CLI](../../../../../docs/adr/Architecture/2026-11-04/cli-interface.md) | Use Typer for commands and Rich for prompts, progress, tables, and errors. |
| [Establish Development Application Startup](../../adr/11-07-26/development-startup-paths.md) | Use development startup paths that include the resume input folder. |

## 10. References

- [Resume Upload Feature Overview](../../../../../docs/system/resume-upload/overview.md)
- [Resume Upload Process](processes/resume-upload.md)
- [CLI Component Technical Specification](../../technical-specification.md)
- [CLI Component Coding Guidelines](../../guidelines.md)
- [Resume Processing Technical System Specification](../../../../core/docs/systems/resume-processing/overview.md)
