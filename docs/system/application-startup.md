# Application Startup Process

## 1. Purpose / Summary

The application startup process prepares CVBrewer for use by initializing the embedded database and ensuring that the input and output folders exist before any workflow begins. If a required startup resource cannot be prepared, startup reports the failure and stops.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B[Resolve Storage Locations]
    B --> C[Initialize Embedded Database]
    C --> D{Initialization Succeeded?}
    D -->|No| E[Report Startup Failure]
    E --> F([Stop Startup])
    D -->|Yes| G[Ensure Input Folder]
    G --> H{Input Folder Ready?}
    H -->|No| E
    H -->|Yes| I[Ensure Output Folder]
    I --> J{Output Folder Ready?}
    J -->|No| E
    J -->|Yes| K([Continue Application Startup])
````

## 3. Rules

- The system must initialize the embedded database before any workflow can begin.
- The system must ensure that the input folder exists as an accessible directory.
- The system must ensure that the output folder exists as an accessible directory.
- The system must report a clear startup failure when database initialization or folder preparation cannot complete.
- The system must stop startup when a required resource cannot be prepared.
- The system must not scan the input folder for resumes during startup.
- The system must not perform resume processing, generation, or deletion during startup.

## 4. Constraints

- Startup must respect operating-system permissions and must not bypass access restrictions.
- Startup must not modify or delete unrelated user files or directories.
- Folder creation during startup is limited to the folders required by resume upload and resume generation.
- Development data locations are temporary and are not the final storage locations for released application data.

## 5. References

- [Command-Line Interface Component Technical Specification](../../cli/docs/technical-specification.md)
- [Application Startup Technical Process](../../cli/docs/processes/application-startup.md)
- [Database Component Technical Specification](../../database/docs/technical-specification.md)
- [Input Folder Initialization](resume-upload/processes/1-input-folder-initialization.md)
- [Output Folder Initialization](resume-generation/processes/1-output-folder-initialization.md)
- [Development Application Startup Decision](../../cli/docs/adr/11-07-26/development-startup-paths.md)
