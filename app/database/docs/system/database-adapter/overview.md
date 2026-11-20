# Database Adapter Technical System Specification

## 1. Purpose

Defines the database-specific implementation of resume persistence for the database component. The adapter owns SQLAlchemy models, SQLite repository implementations, transactions, migrations, and error translation while implementing Core-owned repository contracts.

## 2. Objective

- Implement Core-owned repository contracts using SQLite and SQLAlchemy.
- Persist complete resume records and ordered child data.
- Retrieve resume records by identifier, content fingerprint, and listing.
- Delete every stored resume record and its child data.
- Persist resume processing run and step records, including embedded data and run-to-step relationships.
- Provide all, recent, and error-filtered queries for stored LLM activity logs and processing runs, and per-run step queries.
- Enforce database constraints for relationships, unique fingerprints, and processing log integrity.
- Provide migration infrastructure for persisted schemas.

## 3. Scope

### In Scope

- SQLAlchemy resume models under `app/database/adapters/sqlite/resume/models/`.
- SQLite resume repository under `app/database/adapters/sqlite/resume/`.
- SQLAlchemy models and repositories for resume processing run and step persistence.
- SQLAlchemy models and repositories for LLM activity log persistence and queries.
- SQLAlchemy models and repositories for processing run and step queries.
- Alembic migrations for resume, processing log, and LLM activity log tables.
- Mapping between application records and ORM models.
- Delete-all resume operations and cascade behavior.
- Transaction handling and adapter error translation.

### Out of Scope

- Application-level operation definitions, which are owned by the Core.
- Resume validation, parsing, and processing workflow orchestration.
- Construction of processing run and step records.
- CLI and upload workflow behavior.
- Soft-delete behavior.

## 4. Rules & Constraints

- Repositories must use `session_scope` for transaction boundaries.
- ORM models must remain inside the SQLite adapter.
- Resume child records must preserve `position_order`.
- Child foreign keys must use `ON DELETE CASCADE`.
- `resumes.content_fingerprint` must be unique.
- Delete-all must remove every resume row in one transaction and return the deleted count.
- Database exceptions must be translated through the adapter error hierarchy.
- Mapping code must not mutate the service-layer records.
- Capped log and run queries must order results by their timestamp descending: `created_at` for LLM logs and `started_at` for processing runs.
- Error-filtered queries must match status and error-presence conditions defined by the query process documentation.
- `list_steps(run_id, *, limit=None)` must use step order and attempt number without a limit, and newest `started_at` first with a limit.
- Query capabilities must not require schema or migration changes.
- The CLI must not access database implementations directly.

## 5. Process

| Process | Description | Specification |
| --- | --- | --- |
| Persist Resume | Maps and stores a complete resume record in SQLite. | [Persist Resume](/app/database/docs/system/database-adapter/processes/persist-resume.md) |
| Load Resume | Maps stored SQLite rows into application-level resume records. | [Load Resume](/app/database/docs/system/database-adapter/processes/load-resume.md) |
| Delete All Resumes | Deletes every stored resume row and relies on cascades for child records. | [Delete All Resumes](/app/database/docs/system/database-adapter/processes/delete-all-resumes.md) |
| Persist LLM Log | Maps and stores an LLM activity log record and lists stored records. | [Persist LLM Log](/app/database/docs/system/database-adapter/processes/persist-llm-log.md) |
| Persist Resume Processing Run | Maps and stores a resume processing run record with embedded data and resume identifier references. | [Persist Resume Processing Run](/app/database/docs/system/database-adapter/processes/persist-resume-processing-run.md) |
| Persist Resume Processing Step | Maps and stores a resume processing step record associated with a processing run. | [Persist Resume Processing Step](/app/database/docs/system/database-adapter/processes/persist-resume-processing-step.md) |
| Query LLM Logs | Lists stored LLM activity logs as all, recent, or error-indicating records. | [Query LLM Logs](/app/database/docs/system/database-adapter/processes/query-llm-logs.md) |
| Query Processing Logs | Lists stored processing runs as all, recent, or error-indicating records, and lists steps for one run. | [Query Processing Logs](/app/database/docs/system/database-adapter/processes/query-processing-logs.md) |

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
| DB-ADP-006 | Delete all resumes with child records. | All root and child rows are removed and the deleted count is returned. | Delete-all rule |

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
| [Persist resume processing runs and steps in SQLite](/app/database/docs/adr/11-19-26/resume-processing-run-step-persistence.md) | Store run and step records with a one-to-many relationship and embedded structured fields. |
| [Persist LLM activity logs in SQLite](/app/database/docs/adr/11-19-26/llm-log-persistence.md) | Store LLM logs with an optional processing step reference. |
| [Retain Database Adapters as the Database Component Boundary](/app/database/docs/adr/11-13-26/adapter-only-boundary.md) | Keep adapters in Database and implement Core-owned repository contracts. |
| [Establish resume persistence](/app/database/docs/adr/11-10-26/resume-persistence.md) | Organize adapter repositories and models in dedicated packages and use a hybrid relational schema. |
| [Establish SQLite adapter foundation](/app/database/docs/adr/11-06-26/sqlite-adapter-foundation.md) | Use synchronous SQLAlchemy, explicit SQLite URLs, adapter-local errors, and Alembic scaffolding. |

## 10. Data

The adapter implements the resume schema documented in [Resume Table](/app/database/docs/sqlite/schemas/resumes.md), the processing log schemas documented in [Resume Processing Runs Table](/app/database/docs/sqlite/schemas/resume-processing-runs.md) and [Resume Processing Steps Table](/app/database/docs/sqlite/schemas/resume-processing-steps.md), the LLM log schema documented in [LLM Logs Table](/app/database/docs/sqlite/schemas/llm-logs.md), and related schema documents under [SQLite Database Overview](/app/database/docs/sqlite/overview.md).

## 11. References

- [Database Adapter System Overview](/docs/system/database-adapter/overview.md)
- [Database Component Technical Specification](/app/database/docs/technical-specification.md)
- [Database Service Technical System Specification](/app/core/docs/system/database-service/overview.md)
- [SQLite Database Overview](/app/database/docs/sqlite/overview.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Error Data Model](/docs/data/error.md)
- `app/database/adapters/sqlite/resume/repository.py` — Implements resume persistence and retrieval.
- `app/database/adapters/sqlite/resume/models/` — Defines the SQLite ORM models.
- [Retain Database Adapters as the Database Component Boundary](/app/database/docs/adr/11-13-26/adapter-only-boundary.md)
- [Resume Persistence ADR](/app/database/docs/adr/11-10-26/resume-persistence.md)
- [Persist Resume Processing Runs and Steps in SQLite](/app/database/docs/adr/11-19-26/resume-processing-run-step-persistence.md)
- [Query LLM Logs Process](/docs/system/database-service/processes/query-llm-logs.md)
- [Query Processing Logs Process](/docs/system/database-service/processes/query-processing-logs.md)
