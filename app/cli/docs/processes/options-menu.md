# CLI Options Menu Technical Process

## 1. Purpose

Describe the CLI Options menu workflow. The process presents an Options menu containing Imported Resume and Delete Imported Resumes actions, handles their outcomes, and returns to the previous menu.

## 2. Objective

Provide a secondary interactive menu for CVBrewer options. The process must display the Options menu, handle selection of the available actions, and allow returning to the main menu.

## 3. Scope

### In Scope

- Rendering the Options menu.
- Selecting and running the Imported Resume action.
- Selecting and running the Delete Imported Resumes action.
- Confirming destructive deletion and reporting its outcome.
- Returning to the calling menu.
- Reporting errors from menu actions.

### Out of Scope

- Resume upload processing.
- Database access details.
- Resume generation workflows.

## 4. Rules & Constraints

- The Options menu must include an `Imported Resume` item.
- The Options menu must include a `Delete Imported Resumes` item.
- The Options menu must include a `Back` item.
- The Options menu must use the resume-listing and resume-deletion capabilities supplied through the CLI dependencies.
- The Options menu must not access resume processor internals.
- Selecting `Imported Resume` must display imported resumes when available.
- An empty imported-resume list must be reported as a normal outcome.
- Selecting `Delete Imported Resumes` must explain that only database records are deleted, input folder files are not deleted, and deletion cannot be undone.
- Deletion must require explicit confirmation.
- Deletion must use the shared CLI loading display while the operation runs.
- Selecting `Back` must return to the calling menu.
- Errors from menu actions must be reported without terminating the application.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B[Render Options Menu]
    B --> C[User selects an item]
    C -->|Imported Resume| D[Display imported resumes or empty message]
    D --> B
    C -->|Delete Imported Resumes| E[Explain database-only permanent deletion]
    E --> F{User confirms?}
    F -->|No| G[Report cancellation]
    G --> B
    F -->|Yes| H[Delete with loading and report result]
    H --> B
    C -->|Back| I([Return to caller])
````

### Steps

1. Render the Options menu.
2. Read the user selection.
3. If `Imported Resume` is selected, display imported resumes.
4. If `Delete Imported Resumes` is selected, explain the deletion scope, request confirmation, and delete all imported resumes when confirmed.
5. If `Back` is selected, return to the calling menu.

## 6. Modules

- `app/cli/commands/options.py` — Implements the Options menu and action routing.
- `app/cli/commands/delete_resumes.py` — Implements the Delete Imported Resumes action.
- `app/cli/ui/delete_resumes.py` — Renders deletion confirmation and outcomes.
- `app/cli/ui/progress.py` — Provides the shared loading display.
- `app/cli/modules/context.py` — Defines the injected CLI dependencies and resume capabilities.

## 7. Testing

### 7.1 Test Level

This process is tested at the **Process** level according to the testing strategy.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| Options-001 | The Options menu is displayed. | The user selects Imported Resume. | Imported resumes are displayed. |
| Options-002 | The Options menu is displayed. | The user selects Delete Imported Resumes and confirms. | Imported resumes are deleted and the result is displayed. |
| Options-003 | The Options menu is displayed. | The user selects Delete Imported Resumes and cancels. | No resumes are deleted and cancellation is displayed. |
| Options-004 | The Options menu is displayed. | The user selects Back. | The menu returns to the caller. |

### 7.3 Test Coverage

- Cover Options menu rendering and navigation.
- Cover the empty imported-resume case.
- Cover deletion confirmation, cancellation, result, and error outcomes.

### 7.4 Test Organization

Tests reside in `tests/cli/commands/test_options_menu.py` and `tests/cli/commands/test_delete_resumes.py`.

### 7.5 Test Dependencies

- Use Typer's test runner with newline input where applicable.
- Use explicit CLI dependencies with test doubles for the resume-listing and deletion capabilities.

### 7.6 Testing Rules Compliance

This process follows the testing strategy by verifying observable menu behavior.

## 8. References

- [CLI Component Technical Specification](../technical-specification.md)
- [CLI Component Coding Guidelines](../guidelines.md)
- [CLI Main Menu Technical Process](menu.md)
- [Delete Resumes System Overview](../../../../docs/system/delete-resumes/overview.md)
