# CLI Options Menu Technical Process

## 1. Purpose

Describe the CLI Options menu workflow. The process presents an Options menu containing an Imported Resume action, lets the user view imported resumes, and returns to the previous menu.

## 2. Objective

Provide a secondary interactive menu for CVBrewer options. The process must display the Options menu, handle selection of Imported Resume, and allow returning to the main menu.

## 3. Scope

### In Scope

- Rendering the Options menu.
- Selecting and running the Imported Resume action.
- Returning to the calling menu.
- Reporting errors from the Imported Resume action.

### Out of Scope

- Resume upload processing.
- Database access details.
- Resume generation and deletion workflows.

## 4. Rules & Constraints

- The Options menu must include an `Imported Resume` item.
- The Options menu must include a `Back` item.
- The Options menu must use the resume-listing capability supplied through the CLI dependencies.
- The Options menu must not access resume processor internals.
- Selecting `Imported Resume` must display imported resumes when available.
- An empty imported-resume list must be reported as a normal outcome.
- Selecting `Back` must return to the calling menu.
- Errors from the Imported Resume action must be reported without terminating the application.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B[Render Options Menu]
    B --> C[User selects an item]
    C -->|Imported Resume| D[Display imported resumes or empty message]
    D --> B
    C -->|Back| E([Return to caller])
````

### Steps

1. Render the Options menu.
2. Read the user selection.
3. If `Imported Resume` is selected, display imported resumes.
4. If `Back` is selected, return to the calling menu.

## 6. Modules

- `app/cli/commands/options.py` — Implements the Options menu and Imported Resume action.
- `app/cli/modules/context.py` — Defines the injected CLI dependencies and resume-listing capability.

## 7. Testing

### 7.1 Test Level

This process is tested at the **Process** level according to the testing strategy.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| Options-001 | The Options menu is displayed. | The user selects Imported Resume. | Imported resumes are displayed. |
| Options-002 | The Options menu is displayed. | The user selects Back. | The menu returns to the caller. |

### 7.3 Test Coverage

- Cover Options menu rendering and navigation.
- Cover the empty imported-resume case.

### 7.4 Test Organization

Tests reside in `tests/processes/options-menu/`.

### 7.5 Test Dependencies

- Use Typer's test runner with newline input where applicable.
- Use explicit CLI dependencies with a test double for the resume-listing capability.

### 7.6 Testing Rules Compliance

This process follows the testing strategy by verifying observable menu behavior.

## 8. References

- [CLI Component Technical Specification](../technical-specification.md)
- [CLI Component Coding Guidelines](../guidelines.md)
- [CLI Main Menu Technical Process](menu.md)