# Establish Development Application Startup

## Date

2026-11-07

## Status

Accepted

## Context

CVBrewer needs an application startup path that initializes the embedded database and prepares the resume input and generated output folders. The CLI owns folder management and application orchestration, but the existing CLI boundary rules prohibit the CLI from accessing the Database Service, Database Adapter, or database implementation directly.

The application has no entry point yet, and the current data locations are intended only for development. Final storage locations are not decided.

## Decision

- Place application startup orchestration in the CLI component.
- Use development-only locations under the CLI component:
  - Database file: `cli/data/cvbrewer.db`
  - Resume input folder: `cli/data/local/resumes`
  - Generated output folder: `cli/data/local/generated`
- Ignore `cli/data/` in version control.
- Inject the database initializer into CLI startup as a callable supplied by a composition root outside the CLI component.
- Keep CLI startup free of direct imports from the database component, Database Service, Database Adapter, SQLAlchemy, and SQLite.
- Fail startup when database initialization or folder preparation fails.

## Consequences

- CLI startup respects the existing CLI boundary rules while still initializing the embedded database.
- The composition root is the only place that connects CLI startup to database initialization.
- The development data locations can be replaced without changing the startup workflow.
- Generated database files and local folders are not committed to the repository.
- The current paths must not be treated as final application storage locations.
