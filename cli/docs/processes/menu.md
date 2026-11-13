# CLI Main Menu Technical Process

## 1. Purpose

Describe the CLI main menu workflow. The process presents the CVBrewer main menu and coordinates the Import Resumes, Options, and Exit actions.

## 2. Objective

- Present the main menu after the entry page.
- Let the user import resumes, open the Options menu, or exit.
- Keep the menu available until the user exits.
- Report action failures without terminating the application.

## 3. Scope

### In Scope

- Rendering the CVBrewer main menu.
- Reading the user selection with an interactive selector or numeric prompt.
- Running the Resume Upload and Options menu processes.
- Exiting the application.
- Reporting action errors.

### Out of Scope

- Resume upload file handling and processing.
- Options menu contents.
- Database, Core, LLM, and file-system implementation details.

## 4. Rules & Constraints

- Display the `Import Resumes`, `Options`, and `Exit` items.
- Use an interactive selector when standard input and output are terminals.
- Fall back to a numeric prompt when interactive selection is unavailable.
- Default to `Exit` when the selection cannot be resolved.
- Run the Resume Upload process when `Import Resumes` is selected.
- Run the Options menu process when `Options` is selected.
- Report action errors and return to the menu.
- Exit the application when `Exit` is selected.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    Start([CLI starts without a command]) --> Render[Display CVBrewer main menu]
    Render --> Select[User selects an item]
    Select -->|Import Resumes| Upload[Run resume upload]
    Upload --> Results[Display upload results]
    Results --> Render
    Select -->|Options| Options[Open Options menu]
    Options --> Render
    Select -->|Exit| Exit([Display exit message and stop])
````

### Steps

1. Render the CVBrewer title panel and menu items.
2. Read the user selection.
3. Run the resume upload process when `Import Resumes` is selected.
4. Display upload results and return to the menu.
5. Open the Options menu when `Options` is selected.
6. Return to the main menu after the Options menu closes.
7. Display an exit message and stop when `Exit` is selected.
8. Report action errors and keep the menu available.

## 6. Modules

- `cli/src/cli/processes/menu.py` — Implements main menu rendering, selection, and action routing.
- `cli/src/cli/app.py` — Invokes the main menu when no command is supplied.
- `cli/src/cli/processes/resume_upload.py` — Implements the resume upload action.
- `cli/src/cli/processes/options.py` — Implements the Options menu action.

## 7. Testing

### 7.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| Menu-001 | The main menu is displayed. | The user selects Exit. | The application stops. |
| Menu-002 | The main menu is displayed. | The user selects Options. | The Options menu opens and the main menu returns afterward. |
| Menu-003 | The main menu is displayed and the input folder is empty. | The user selects Import Resumes. | The empty-folder result is displayed and the menu returns. |
| Menu-004 | An action raises an error. | The action is selected. | The error is reported and the menu remains available. |

### 7.3 Test Coverage

- Cover menu rendering, Exit, Options navigation, and Import Resumes routing.
- Cover error reporting without application termination.

### 7.4 Test Organization

Tests reside in `tests/processes/menu/`.

### 7.5 Test Dependencies

- Use Typer's `CliRunner` with newline input.
- Use temporary input folders and test doubles for the resume processor.

### 7.6 Testing Rules Compliance

This process follows the testing strategy by verifying observable menu behavior and action routing.

## 8. References

- [CLI Component Technical Specification](../technical-specification.md)
- [CLI Entry Page Technical Process](entry-page.md)
- [CLI Options Menu Technical Process](options-menu.md)
- [Resume Upload Technical Process](../systems/resume-upload/processes/resume-upload.md)
- [CLI Component Coding Guidelines](../guidelines.md)
- [Use Typer and Rich for a hybrid CLI](../../../docs/adr/Architecture/2026-11-04/cli-interface.md)
