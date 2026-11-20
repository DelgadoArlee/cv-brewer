# Record Resume Processing Runs and Steps in Core

## Date

2026-11-19

## Status

Accepted

## Context

The high-level [Resume Processing Run and Step Logging](/docs/adr/Architecture/2026-11-19/resume-processing-run-logging.md) decision requires Core to document how resume processing executions are observed and recorded. Resume processing is orchestrated in Core and already coordinates stage progression, outcomes, LLM enhancement, and storage through Core-owned service boundaries.

## Decision

- Document run and step record construction as a Core resume-processing responsibility.
- A processing run is created when resume processing begins for a file and finalized with status, result, timing, summary, performance, referenced resume identifiers, and embedded error data.
- A processing step is recorded for each executed processing stage or attempted operation, including order, attempt, timing, input/output summaries, duration, memory and CPU performance measurements, metadata, and embedded error data.
- Core records `resume_id` and `matched_resume_id` as identifier references supplied by processing outcomes; it does not create database relationships to resume records.
- LLM activity logs reference their processing step directly through `processing_step_id`; step records do not carry LLM log identifier lists.
- Core-owned run and step log records are delivered through Core service boundaries to configured persistence destinations; database-specific storage remains in the Database Adapter.
- A duplicate run is finalized with status `SUCCESS` and result `duplicate`; downstream steps are recorded as `SKIPPED`.
- Resume processing history is represented by run and step records; no separate per-resume processing history is maintained.

## Consequences

- Core technical documentation must describe run/step creation, update, and finalization points in the resume-processing workflow.
- Step naming, ordering, and outcome mapping must be documented consistently with resume-processing stages.
- Database adapters receive complete run and step records without owning run/step construction rules.
