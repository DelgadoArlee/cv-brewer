# Database Adapter System Overview

## 1. Purpose

The Database Adapter implements database-specific operations for the Database Service. It owns connections, ORM use, queries, transactions, migrations, and database-specific error translation so that application-level operations remain independent of a database implementation. The adapter implements repository contracts owned by the Core.

## 2. Objectives

- Persist application-level data in the selected database implementation.
- Retrieve stored data for application-level operations.
- Persist resume processing run and step records for processing execution review.
- Provide query operations for stored LLM activity logs and processing run and step records.
- Preserve database constraints, relationships, ordering, and identifier-reference boundaries.
- Translate database failures into adapter-level errors.
- Manage schema creation and migration for persisted data.

## 3. Scope

### In Scope

- SQLite connections, SQLAlchemy engine and session lifecycle, and migrations.
- SQLAlchemy models for resume persistence.
- SQLAlchemy models for resume processing run and step persistence.
- Repository implementations for resume operations.
- Repository implementations for resume processing run and step persistence.
- Repository implementations for LLM activity log persistence and queries.
- Repository implementations for processing run and step queries.
- Transaction handling and error translation for persistence and query operations.

### Out of Scope

- Application-level data operation definitions.
- Resume validation, parsing, or generation.
- Resume processing workflow orchestration and run/step record construction.
- CLI workflows and file-system management.
- Business-rule decisions about when resume data or processing log records may be stored.

## 4. Workflow

The adapter receives repository requests from the Database Service, maps application records to database models, performs the requested operation inside a transaction, and returns mapped application records.

Resume operations persist and load resume aggregates. Processing log operations persist run records and associated step records, preserving the run-to-step relationship and embedded log data.

Resume operations persist and load resume aggregates. Processing log operations persist run records and associated step records, preserving the run-to-step relationship and embedded log data. Log query operations return stored LLM logs and processing run or step records; capped queries return the newest matching records.

See the [Persist Resume Process](/docs/system/database-adapter/processes/persist-resume.md), [Load Resume Process](/docs/system/database-adapter/processes/load-resume.md), [Persist Resume Processing Run Process](/docs/system/database-adapter/processes/persist-resume-processing-run.md), [Persist Resume Processing Step Process](/docs/system/database-adapter/processes/persist-resume-processing-step.md), [Query LLM Logs Process](/docs/system/database-service/processes/query-llm-logs.md), and [Query Processing Logs Process](/docs/system/database-service/processes/query-processing-logs.md).

## 5. Constraints

- All database-specific implementation details must remain inside the adapter.
- Application-level data management rules must remain in the Core Database Service.
- Models must not be exposed to other components.
- Transactions must commit successful work and roll back failed work.
- The adapter must not expose direct database access to the CLI; queries must be reached through the Database Service.
- Query capabilities must not require schema or migration changes.

## 6. Rules

- Adapter repositories must use the existing transactional session boundary.
- Resume child data must be stored with its ordering preserved.
- Foreign keys must enforce resume child relationships and the `resume_processing_steps.run_id` relationship to `resume_processing_runs.run_id` with `ON DELETE CASCADE`.
- Content fingerprints must be enforced as unique.
- `resume_processing_runs.resume_id` and `matched_resume_id` must be stored without foreign-key relationships to resume tables.
- `resume_processing_steps.input.source_step_id` must be stored as an identifier reference without a required foreign-key relationship.
- `llm_logs.processing_step_id` must be stored as an indexed, nullable foreign key to `resume_processing_steps.step_id` with `ON DELETE SET NULL`.
- Embedded processing log structures (`summary`, `performance`, `input`, `output`, `error`, `metadata`) must be persisted according to the SQLite schema mapping.
- Database exceptions must be translated to adapter-level errors.

## 7. Data Management

The adapter stores resume records and resume processing execution records using the SQLite schema documented in [SQLite Database Overview](/app/database/docs/sqlite/overview.md). Processing run and step records are the persisted execution logs and may reference resume identifiers without database relationships.

## 8. Error Handling

- Integrity failures must be translated and reported.
- Operational, data, programming, and other database failures must be translated and reported.
- Failed operations must not leave partial resume records committed.

## 9. References

- [Database Component Technical Specification](/app/database/docs/technical-specification.md)
- [Database Adapter Technical Specification](/app/database/docs/system/database-adapter/overview.md)
- [User Resume Data Model](/docs/data/user-resume.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Error Data Model](/docs/data/error.md)
- [Add Resume Processing Run and Step Logging](/docs/adr/Architecture/2026-11-19/resume-processing-run-logging.md)
- [Query LLM Logs Process](/docs/system/database-service/processes/query-llm-logs.md)
- [Query Processing Logs Process](/docs/system/database-service/processes/query-processing-logs.md)
