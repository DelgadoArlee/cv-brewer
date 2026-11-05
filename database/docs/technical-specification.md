# Database Component Technical Specification

## 1. Purpose

This document defines the technical organization of the database component within CVBrewer. It describes how the Database Service and Database Adapter are structured and bounded so structured application data can be accessed without coupling the rest of the application to a specific database implementation.

## 2. Objective

- Provide a stable application-level data access boundary for the Core Processing Engine.
- Keep database-specific concerns inside adapter implementations.
- Support SQLite as the default database implementation through SQLAlchemy 2.0 and Alembic.
- Allow future database implementations to be added through compatible adapters without changing application-level data operations.
- Keep the database component within the single Python distribution used by the application.

## 3. Scope

### In Scope

- The database component package and its internal subpackages.
- Database Service application-level data operations and boundaries.
- Database Adapter implementation boundaries.
- Database connections, ORM configuration, queries, transactions, migrations, and error translation within adapters.
- Component technical documentation.

### Out of Scope

- Core Processing Engine resume processing and generation workflows.
- CLI user interaction and file-system management.
- LLM integration.
- Data model definitions and schema validation rules, which are documented separately.
- Original PDF and generated Markdown file management.
- Implementation code, database models, migrations, and test cases.

## 4. Rules & Constraints

- The Database Service must define the application-level create, read, update, delete, and query operations required by the application.
- The Database Service must not contain database-specific queries, connection handling, or ORM behavior.
- All database operations must be performed through the selected Database Adapter.
- The Database Adapter must own database connections, connection lifecycle, ORM configuration, query execution, transactions, migrations, and database-specific error translation.
- The Core Processing Engine must depend only on the Database Service interface and must not import SQLAlchemy or SQLite directly.
- SQLite is the default database implementation, accessed through SQLAlchemy 2.0, with schema changes managed by Alembic inside the Database Adapter.
- Database-specific implementation details must remain isolated to adapter packages.
- Application-level data structures must follow the approved data model documentation.
- Application-level data management rules must not be implemented in the Database Adapter.
- The database component must remain part of the single Python distribution and must not be independently deployed.

## 5. Architectural & Design Approaches

### 5.1. Service–Adapter Separation

- **Name:** Service–Adapter separation.
- **Description:** Application-level data operations are separated from database-specific implementation details.
- **Application:** The Database Service defines the operations required by the application, and the Database Adapter carries out those operations using the selected database implementation.

### 5.2. Adapter Pattern

- **Name:** Adapter pattern.
- **Description:** A stable component interface is implemented by database-specific adapters.
- **Application:** The SQLite adapter uses SQLAlchemy and Alembic, and future database implementations can be supported by providing compatible adapters without changing the Database Service.

### 5.3. Single-Project Internal Packaging

- **Name:** Single-project internal packaging.
- **Description:** The database component is maintained as one Python project containing internal packages.
- **Application:** The Database Service and database adapter implementations are organized under `database/src/database/` as separate internal packages.

## 6. Systems

| System | Description | Specification |
| --- | --- | --- |
| Database Service | Manages application-level data operations and coordinates requests through the selected Database Adapter. | Not yet documented |
| Database Adapter | Implements database-specific operations, connections, ORM use, transactions, migrations, and error translation. | Not yet documented |

## 7. File Structure

````text
database/
├── pyproject.toml          Project configuration and package metadata.
├── README.md               Package README file.
├── .python-version         Python version selection.
├── docs/
│   └── technical-specification.md
└── src/
    └── database/
        ├── __init__.py
        ├── database_service/
        │   └── __init__.py
        └── adapters/
            └── __init__.py
````

## 8. Deployment

- The database component is included in the single CLI/Core executable.
- SQLite is embedded in the application environment and does not require a separately running database server.
- An external database may be used when a compatible Database Adapter is implemented and configured; the external database server is deployed and operated separately from the application executable.

## 9. References

- [System Architecture](../../docs/architecture.md)
- [Repository Architecture](../../docs/repository/architecture.md)
- [Tech Stack](../../docs/tech-stack.md)
- [Use SQLite through SQLAlchemy and Alembic](../../docs/adr/Architecture/2026-11-04/database-persistence.md)
- [Use Python and uv for the CVBrewer implementation](../../docs/adr/Architecture/2026-11-04/python-runtime-and-tooling.md)
- [User Resume Data Model](../../docs/data/user-resume.md)
- [General System Rules](../../docs/system-rules.md)
