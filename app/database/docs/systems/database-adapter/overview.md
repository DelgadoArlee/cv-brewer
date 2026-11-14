# Database Adapter Technical System Specification

## 1. Purpose

Defines the database-specific implementation of resume persistence for the database component. The adapter owns SQLAlchemy models, SQLite repository implementations, transactions, migrations, and error translation while implementing Core-owned repository contracts.

## 2. Objective

- Implement the Core-owned resume repository contract using SQLite and SQLAlchemy.
- Persist complete resume records and ordered child data.
- Retrieve resume records by identifier, content fingerprint, and listing.
- Enforce database constraints for relationships and unique fingerprints.
- Provide migration infrastructure for the resume schema.

## 3. Scope

### In Scope

- SQLAlchemy resume models under `app/database/adapters/sqlite/resume/models/`.
- SQLite resume repository under `app/database/adapters/sqlite/resume/`.
- Alembic migration for resume tables.
- Mapping between application records and ORM models.
- Transaction handling and adapter error translation.

### Out of Scope

- Application-level operation definitions, which are owned by the Core.
- Resume validation and parsing.
- CLI and upload workflow behavior.
- Delete-all resume behavior.

## 4. Rules & Constraints

- Repositories must use `session_scope` for transaction boundaries.
- ORM models must remain inside the SQLite adapter.
- Resume child records must preserve `position_order`.
- Child foreign keys must use `ON DELETE CASCADE`.
- `resumes.content_fingerprint` must be unique.
- Database exceptions must be translated through the adapter error hierarchy.
- Mapping code must not mutate the service-layer records.

## 5. Process

| Process | Description | Specification |
| --- | --- | --- |
| Persist Resume | Maps and stores a complete resume record in SQLite. | [Persist Resume](processes/persist-resume.md) |
| Load Resume | Maps stored SQLite rows into application-level resume records. | [Load Resume](processes/load-resume.md) |

## 6. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| SQLAlchemy | External library | Declarative models, sessions, transactions, queries, and error types. |
| Alembic | External library | Schema migrations. |
| `ResumeRepository` | Core-owned interface | Defines the adapter contract implemented by the SQLite repository. |
| `ResumeRecord` | Core-owned record | Application-level data mapped to SQLite models. |

## 7. Test Cases

| Test Case ID | Scenario | Expected Result | Related Rule |
| --- | --- | --- | --- |
| DB-ADP-001 | Run the resume migration on an empty database. | All resume tables, indexes, and foreign keys exist. | Migration rule |
| DB-ADP-002 | Persist and load a complete resume record. | All root and child data round-trip correctly. | Mapping rule |
| DB-ADP-003 | Persist a duplicate content fingerprint. | An adapter integrity failure is raised and no duplicate is stored. | Unique fingerprint rule |
| DB-ADP-004 | Load a missing resume. | `None` is returned. | Missing record rule |
| DB-ADP-005 | Delete a resume row directly. | Child rows are removed by cascade. | Cascade rule |

## 8. Diagrams

````mermaid
flowchart LR
    Port[ResumeRepository] --> Repo[SqliteResumeRepository]
    Repo --> Session[session_scope]
    Session --> Models[SQLAlchemy Resume Models]
    Models --> SQLite[(SQLite)]
````

## 9. Architecture Decision Log

| ADR | Decision Summary |
| --- | --- |
| [Retain Database Adapters as the Database Component Boundary](../../adr/11-13-26/adapter-only-boundary.md) | Keep adapters in Database and implement Core-owned repository contracts. |
| [Establish resume persistence](../../adr/11-10-26/resume-persistence.md) | Organize adapter repositories and models in dedicated packages and use a hybrid relational schema. |
| [Establish SQLite adapter foundation](../../adr/11-06-26/sqlite-adapter-foundation.md) | Use synchronous SQLAlchemy, explicit SQLite URLs, adapter-local errors, and Alembic scaffolding. |

## 10. Data

The adapter implements the resume schema documented in [Resume Table](../../sqlite/schemas/resumes.md) and its related schema documents under [SQLite Database Overview](../../sqlite/overview.md).

## 11. References

- [Database Adapter System Overview](../../../../../docs/system/database-adapter/overview.md)
- [Database Component Technical Specification](../../technical-specification.md)
- [Database Service Technical System Specification](../../../../core/docs/systems/database-service/overview.md)
- [SQLite Database Overview](../../sqlite/overview.md)
- `app/database/adapters/sqlite/resume/repository.py` — Implements resume persistence and retrieval.
- `app/database/adapters/sqlite/resume/models/` — Defines the SQLite ORM models.
- [Retain Database Adapters as the Database Component Boundary](../../adr/11-13-26/adapter-only-boundary.md)
- [Resume Persistence ADR](../../adr/11-10-26/resume-persistence.md)
