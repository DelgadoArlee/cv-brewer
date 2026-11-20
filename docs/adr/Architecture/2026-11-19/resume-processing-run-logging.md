# Add Resume Processing Run and Step Logging

## Date

2026-11-19

## Status

Accepted

## Category

architecture

## Context

Resume processing needs a dedicated audit record for each processing execution with structured step-level input/output summaries, performance measurements, and embedded error details. The application needs documentation for a run-and-step logging model that can represent processing outcomes, including cases where a saved parsed resume is not produced or a duplicate match is identified.

## Decision

- Introduce a Resume Processing Run data model to represent one execution of the `resume_processing` process, including identity, process version, status, result, timing, summary counts, run-level performance, optional `resume_id` and `matched_resume_id` references, and an embedded `error`.
- Introduce a Resume Processing Step data model to represent each recorded step within a run, including identity, run association, step name/order/attempt, status, timing, input/output summaries, step-level performance, metadata, and an embedded `error`.
- Define Processing Run and Processing Step as a one-to-many relationship: each step belongs to exactly one run and a run may have multiple steps.
- Define a shared embedded Error Data Model for run-level and step-level failures.
- Allow `resume_id` and `matched_resume_id` to reference stored resume identifiers without creating database relationships to the resume tables.
- Treat `input.source_step_id` as an identifier reference rather than a required database relationship.
- Link LLM activity logs to processing steps through a nullable processing step reference on LLM log records; one step can have many LLM logs, and one LLM log can reference zero or one step.
- Document SQLite persistence as dedicated `resume_processing_runs` and `resume_processing_steps` tables, with nested run/step structures and embedded errors mapped as structured columns/fields appropriate to the database implementation.
- Replace the former per-resume history model with run and step records as the persisted resume processing log.

## Consequences

- High-level and database documentation must define run, step, and embedded error structures and their persistence mapping.
- Resume processing documentation must describe where run and step records are created, updated, and finalized across processing outcomes.
- A run can be documented for stored, duplicate, rejected, or failed outcomes without requiring a stored resume foreign-key relationship.
- Resume processing history is no longer part of the data model or storage; run and step records are the persisted processing logs.
