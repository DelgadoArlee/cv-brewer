# Resume Upload Technical Process

## 1. Purpose

Define how the CLI prepares the input folder, reads resume files, delegates processing to the Core Processing Engine, and reports outcomes.

## 2. Objective

- Ensure the input folder is available.
- Discover and read every file in the input folder.
- Process each file independently through the Core.
- Report progress and final results to the user.

## 3. Scope

### In Scope

- Input folder creation and accessibility checks.
- File discovery, ordering, and byte reading.
- `ResumeInput` creation and Core delegation.
- Per-file failure handling.
- Progress and result rendering.

### Out of Scope

- File validation, parsing, schema validation, deduplication, and storage.
- Database and LLM access.
- File deletion, renaming, or moving.
- Resume generation and deletion workflows.

## 4. Rules & Constraints

- Use the resume input folder from the CLI startup paths.
- Create the folder with parent directories when missing.
- Reject paths that are not directories.
- Discover regular files only, ordered by file name.
- Do not filter files by extension or type.
- Read file bytes in the CLI.
- Process files sequentially and independently.
- Continue after per-file failures.
- Report unreadable files as processing-failure outcomes.
- Return a normal completion outcome without processing when the folder is empty.
- Require a resume processor only when files are present.
- Report Core stages when a console is available.
- Display the result table when a console is available.
- Do not modify or delete uploaded files.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    User([User selects Import Resumes]) --> Ensure{Input folder accessible?}
    Ensure -->|No, missing| Create[Create input folder]
    Create --> Discover
    Ensure -->|Yes| Discover[Discover files ordered by name]
    Ensure -->|Failure| Error[Report upload error]
    Discover --> Empty{Any files?}
    Empty -->|No| EmptyMessage[Display empty-folder message]
    Empty -->|Yes| Read[Read file bytes]
    Read --> Progress[Display progress and current stage]
    Progress --> Core[Process each file through Core]
    Core --> Results[Display result table]
    EmptyMessage --> End([Return to menu])
    Results --> End
````

### Steps

1. Resolve the input folder from the startup paths.
2. Create the folder when it does not exist and verify it is a directory.
3. Discover regular files and order them by file name.
4. Return a normal empty-folder result when no files are present.
5. Read the bytes of every discovered file.
6. Create a `ResumeInput` for each readable file.
7. Process each input through the Core, forwarding stage notifications.
8. Record processing-failure outcomes for unreadable files.
9. Display the result table with stored, duplicate, and failed counts.
10. Return to the main menu.

## 6. Modules

- `cli/src/cli/processes/resume_upload.py` — Implements folder preparation, discovery, reading, delegation, and outcome collection.
- `cli/src/cli/ui/resume_upload.py` — Implements progress stage labels and result rendering.
- `cli/src/cli/modules/paths.py` — Provides the resume input folder path.
- `core/src/core/pipeline/resume_processing.py` — Processes resume inputs and reports outcomes.
- `core/src/core/models/resume.py` — Defines resume inputs, outcomes, and statuses.

## 7. Testing

### 7.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| RU-001 | An input folder with multiple files. | Upload runs. | Every file is processed and an outcome is returned for each. |
| RU-002 | An input folder that does not exist. | Upload runs. | The folder is created and discovery proceeds. |
| RU-003 | An empty input folder. | Upload runs. | The upload completes normally with an empty-folder message. |
| RU-004 | A file that cannot be read. | Upload runs. | A processing-failure outcome is returned for that file. |
| RU-005 | A console and a processing Core. | Upload runs. | Stage notifications update progress and results are displayed. |
| RU-006 | Files are present but no processor is supplied. | Upload runs. | An upload error is raised. |

### 7.3 Test Coverage

- Cover folder creation, discovery, empty folders, unreadable files, and per-file independence.
- Cover stage progress and result rendering.
- Use temporary folders and test doubles for the Core processor.

### 7.4 Test Organization

Tests reside in `tests/processes/resume-upload/`.

### 7.5 Test Dependencies

- Use temporary input folders for file discovery.
- Use a test double for the resume processor when Core behavior is not under test.

### 7.6 Testing Rules Compliance

This process follows the testing strategy by verifying observable upload behavior and outcome reporting.

## 8. References

- [Resume Upload Technical System Specification](../overview.md)
- [Resume Upload Feature Overview](../../../../../docs/system/resume-upload/overview.md)
- [CLI Main Menu Technical Process](../../../processes/menu.md)
- [CLI Component Technical Specification](../../../technical-specification.md)
- [CLI Component Coding Guidelines](../../../guidelines.md)
