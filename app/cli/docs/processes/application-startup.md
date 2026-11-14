# Application Startup Technical Process

## 1. Purpose

Describe the CLI implementation of the application startup process. The process initializes the embedded database through an injected initializer and prepares the resume input and generated output folders before normal CLI operation begins.

## 2. Objective

Prepare all required startup resources so that database access, resume upload, and resume generation can proceed. Stop startup with a clear error when a required resource cannot be prepared.

## 3. Scope

### In Scope

- Resolving development startup locations.
- Invoking the injected database initializer with the database path.
- Creating the resume input folder.
- Creating the generated output folder.
- Reporting startup failures.

### Out of Scope

- Direct database implementation access.
- Database migrations, schemas, and table definitions.
- Resume discovery, processing, generation, or deletion.
- Final operating-system user-data locations.
- CLI command and menu implementation.

## 4. Rules & Constraints

- The process must accept the database initializer from the application composition root.
- The application composition root must run the process before creating the CLI application.
- The process must not import the database component, Database Service, Database Adapter, SQLAlchemy, or SQLite.
- The process must initialize the database before creating the input and output folders.
- The process must fail when database initialization fails.
- The process must fail when a required folder cannot be created as a directory.
- The process must not create input or output folders when database initialization fails.
- The process must not scan the input folder for resumes.
- Development data locations must remain outside version control.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B[Resolve Startup Paths]
    B --> C[Call Injected Database Initializer]
    C --> D{Database Initialized?}
    D -->|No| E[Raise Startup Error]
    D -->|Yes| F[Ensure Resume Input Folder]
    F --> G{Input Folder Ready?}
    G -->|No| E
    G -->|Yes| H[Ensure Generated Output Folder]
    H --> I{Output Folder Ready?}
    I -->|No| E
    I -->|Yes| J([Return Startup Paths])
````

### Steps

1. Receive the startup paths and injected database initializer.
2. Invoke the initializer with the configured database path.
3. Stop with `StartupError` when the initializer fails.
4. Create the resume input folder and any missing parent directories.
5. Stop with `StartupError` when the input folder cannot be created as a directory.
6. Create the generated output folder and any missing parent directories.
7. Stop with `StartupError` when the output folder cannot be created as a directory.
8. Return the prepared startup paths.

## 6. Modules

- `app/cli/modules/paths.py` — Defines the startup path container and shared startup layout.

## 8. Testing

### 8.1 Test Level

This process is tested at the **Process** level according to the testing strategy.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| Process-001 | Managed test data paths and a successful database initializer. | Startup runs. | The initializer receives the database path, and the input and output folders exist under `tests/data/`. |
| Process-002 | A database initializer that fails. | Startup runs. | Startup raises `StartupError` and does not create input or output folders. |
| Process-003 | A required folder path exists as a file. | Startup runs. | Startup raises `StartupError` and does not create the remaining folder. |
| Process-004 | Development startup paths are requested. | Paths are resolved. | Paths remain under `cli/data/` with the configured names. |
| Process-005 | Test and development startup paths are resolved. | Relative structures are compared. | The test data layout matches the development layout. |

### 8.3 Test Coverage

- Cover successful startup using the managed test data environment, database failure, filesystem conflict, and test/development structure parity.
- Use the managed `tests/data/` environment for successful startup and temporary resources for failure scenarios.
- Do not test private helper behavior independently.

### 8.4 Test Organization

Tests reside in `tests/processes/application-startup/`.

The tests are marked `application_startup` and run before all other tests.

### 8.5 Test Dependencies

- Use the session-scoped `test_startup_paths` fixture for the successful startup scenario under `tests/data/`.
- Use `tmp_path` for failure scenarios.
- Use real database initialization for the shared success scenario and test doubles for failure scenarios.

### 8.6 Testing Rules Compliance

This process follows the testing strategy by verifying observable startup outcomes, using the managed test data environment for the success scenario, isolated temporary resources for failure scenarios, and avoiding implementation-detail tests.

## 9. References

- [Application Startup Process](../../../../docs/system/application-startup.md)
- [CLI Component Technical Specification](../technical-specification.md)
- `app/cli/modules/paths.py`
- [Development Application Startup Decision](../adr/11-07-26/development-startup-paths.md)
- [Inject CLI Dependencies Explicitly](../adr/11-14-26/explicit-cli-dependencies.md)
- [CLI Component ADL](../adr/ADL.md)
