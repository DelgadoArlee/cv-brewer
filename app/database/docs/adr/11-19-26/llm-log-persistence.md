# Persist LLM Activity Logs in SQLite

## Date

2026-11-19

## Status

Accepted

## Context

The [LLM activity logging](/docs/adr/Architecture/2026-11-19/llm-activity-logging.md) decision requires a new persisted log record. The [database adapter boundary](/app/database/docs/adr/11-13-26/adapter-only-boundary.md) decision requires Core to own application records and repository contracts while the Database component owns ORM models, migrations, and queries.

## Decision

- Define the LLM log repository contract in Core under `app/core/services/llm/`.
- Add an `llm_logs` table to the SQLite adapter.
- Link each log record to a processing step through nullable indexed `processing_step_id` referencing `resume_processing_steps.step_id` with `ON DELETE SET NULL`.
- Store request parameters as a JSON object whose fields are null in the current application.
- Store timestamps as `DATETIME`, duration and memory/CPU measurements as `FLOAT`, and token counts and `sample_count` as `INTEGER`.
- Constrain status to `SUCCESS`, `FAILED`, or `TIMEOUT`.
- Add an Alembic migration for table creation and include the new ORM model in migration metadata.
- Implement save and list operations in a SQLite repository that follows the existing session and error-translation patterns.

## Consequences

- The database component owns the table schema, migration, queries, and schema documentation.
- The log repository can back both the LLM logger and the logger CLI query capability.
- No resume tables are changed and no relationship to resumes is introduced; log records may reference processing steps.
