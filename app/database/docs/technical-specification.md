# Database Component Technical Specification

## 1. Purpose

This document defines the technical organization of the database component within CVBrewer. It describes how Database Adapters are structured and bounded so database-specific operations can be implemented without coupling the Core application layer to a specific database implementation. Application-level resume data operations are owned by the Core.

## 2. Objective

- Provide adapter implementations for Core-owned resume repository contracts.
- Keep database-specific concerns inside adapter implementations.
- Support SQLite as the default database implementation through SQLAlchemy 2.0 and Alembic.
- Allow future database implementations to be added through compatible adapters without changing application-level data operations.
- Keep the database component within the single Python distribution used by the application.

## 3. Scope

### In Scope

- The database component package and its internal subpackages.
- Database Adapter implementation boundaries.
- Database connections, ORM configuration, queries, transactions, migrations, and error translation within adapters.
- Component technical documentation.

### Out of Scope

- Application-level resume data operations, record definitions, and repository contracts, which belong to the Core.
- Core Processing Engine resume processing and generation workflows.
- CLI user interaction and file-system management.
- LLM integration.
- Data model definitions and schema validation rules, which are documented separately.
- Original PDF and generated Markdown file management.
- Implementation code, database models, migrations, and test cases.

## 4. Rules & Constraints

- The Database Adapter must implement the repository contracts defined by the Core.
- The database component must not define application-level operations or application-level record structures.
- All database operations must be performed through the selected Database Adapter.
- The Database Adapter must own database connections, connection lifecycle, ORM configuration, query execution, transactions, migrations, and database-specific error translation.
- The Core must not import SQLAlchemy, SQLite, or database adapters directly.
- SQLite is the default database implementation, accessed through SQLAlchemy 2.0, with schema changes managed by Alembic inside the Database Adapter.
- Database-specific implementation details must remain isolated to adapter packages.
- Application-level data structures must follow the approved data model documentation.
- Application-level data management rules must not be implemented in the Database Adapter.
- Database Adapter code organization must follow the [Database Component Coding Guidelines](guidelines.md).
- The database component must remain part of the single Python distribution and must not be independently deployed.

## 5. Architectural & Design Approaches

### 5.1. Adapter Layer for Core-Owned Service Contracts

- **Name:** Adapter layer for Core-owned service contracts.
- **Description:** Application-level resume operations are separated from database-specific implementation details.
- **Application:** The Core defines the resume repository contract and service operations, and the Database Adapter carries out those operations using the selected database implementation.

### 5.2. Adapter Pattern

- **Name:** Adapter pattern.
- **Description:** A stable Core-owned interface is implemented by database-specific adapters.
- **Application:** The SQLite adapter uses SQLAlchemy and Alembic, and future database implementations can be supported by providing compatible adapters without changing the Core service.

### 5.3. Single-Project Internal Packaging

- **Name:** Single-project internal packaging.
- **Description:** The database component is maintained as a module within the single application Python project.
- **Application:** Database adapter implementations are organized under `app/database/` and packaged with the other components by the `app/` project.

## 6. Systems

| System           | Description                                                                                                     | Specification                                                                        |
| ---------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Database Adapter | Implements Core-owned repository contracts, database-specific operations, connections, ORM use, transactions, migrations, and error translation. | [Database Adapter](systems/database-adapter/overview.md)                             |

## 7. File Structure

````text
app/database/
├── README.md               Component README file.
├── docs/
│   ├── technical-specification.md
│   ├── guidelines.md
│   ├── adr/
│   │   ├── ADL.md
│   │   ├── 11-06-26/
│   │   │   └── sqlite-adapter-foundation.md
│   │   ├── 11-10-26/
│   │   │   └── resume-persistence.md
│   │   └── 11-13-26/
│   │       └── adapter-only-boundary.md
│   ├── sqlite/
│   │   ├── overview.md
│   │   └── schemas/
│   │       ├── resume-certifications.md
│   │       ├── resume-education.md
│   │       ├── resume-experience.md
│   │       ├── resume-processing-history.md
│   │       ├── resume-skills.md
│   │       └── resumes.md
│   └── systems/
│       └── database-adapter/
│           ├── overview.md
│           └── processes/
│               ├── load-resume.md
│               └── persist-resume.md
├── __init__.py
└── adapters/
    ├── __init__.py
    └── sqlite/
        ├── __init__.py
        ├── alembic.ini
        ├── config.py
        ├── engine.py
        ├── errors.py
        ├── migrations.py
        ├── migrations/
        │   ├── env.py
        │   ├── script.py.mako
        │   └── versions/
        │       └── 20261110_0001_create_resume_tables.py
        └── resume/
            ├── __init__.py
            ├── repository.py
            └── models/
                ├── __init__.py
                ├── base.py
                ├── resume.py
                ├── resume_certification.py
                ├── resume_education.py
                ├── resume_experience.py
                ├── resume_processing_history.py
                └── resume_skill.py
````

## 8. Deployment

- The database component is included in the single CLI/Core executable.
- SQLite is embedded in the application environment and does not require a separately running database server.
- An external database may be used when a compatible Database Adapter is implemented and configured; the external database server is deployed and operated separately from the application executable.

## 9. References

- [System Architecture](../../../docs/architecture.md)
- [Repository Architecture](../../README.md)
- [Tech Stack](../../../docs/tech-stack.md)
- [Core Component Technical Specification](../../core/docs/technical-specification.md)
- [Database Component Coding Guidelines](guidelines.md)
- [Database Adapter System Specification](systems/database-adapter/overview.md)
- [SQLite Database Overview](sqlite/overview.md)
- [Move the Database Service into Core](../../../docs/adr/Architecture/2026-11-13/database-service-to-core.md)
- [Retain Database Adapters as the Database Component Boundary](adr/11-13-26/adapter-only-boundary.md)
- [Use SQLite through SQLAlchemy and Alembic](../../../docs/adr/Architecture/2026-11-04/database-persistence.md)
- [Use Python and uv for the CVBrewer implementation](../../../docs/adr/Architecture/2026-11-04/python-runtime-and-tooling.md)
- [User Resume Data Model](../../../docs/data/user-resume.md)
- [General System Rules](../../../docs/system-rules.md)
