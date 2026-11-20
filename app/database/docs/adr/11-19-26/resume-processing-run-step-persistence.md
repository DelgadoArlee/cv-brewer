# Persist Resume Processing Runs and Steps in SQLite

## Date

2026-11-19

## Status

Accepted

## Context

The [Resume Processing Run and Step Logging](/docs/adr/Architecture/2026-11-19/resume-processing-run-logging.md) decision requires dedicated persistence for processing runs and processing steps. The [adapter-only boundary](/app/database/docs/adr/11-13-26/adapter-only-boundary.md) decision requires Core to own application records and contracts while the Database component owns ORM models, migrations, queries, and schema documentation.

## Decision

- Add `resume_processing_runs` and `resume_processing_steps` tables to the SQLite adapter.
- Store each run as one row with `run_id` as the primary identifier and nested `summary`, `performance`, and `error` structures persisted as structured database fields.
- Store each step as one row with `step_id` as the primary identifier, `run_id` referencing `resume_processing_runs`, and nested `input`, `output`, `performance`, `error`, and `metadata` structures persisted as structured database fields.
- Enforce the one-to-many run-to-step relationship with a foreign key from `resume_processing_steps.run_id` to `resume_processing_runs.run_id` with `ON DELETE CASCADE`.
- Store `resume_id` and `matched_resume_id` as identifier values without foreign-key relationships to resume tables.
- Store `input.source_step_id` as an identifier reference without a required database relationship.
- Document save and retrieval operations in the Database Adapter and include migrations and ORM models in the SQLite implementation scope.

## Consequences

- The database component owns run/step table schemas, migrations, ORM mappings, and persistence processes.
- Run and step records can be persisted independently of resume-row foreign-key constraints while preserving the required run-to-step integrity.
- Resume processing history is represented by run and step records; no separate per-resume processing history table is maintained.
