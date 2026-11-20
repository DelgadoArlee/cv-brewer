# Resume Processing Steps Table Schema

## 1. Database Object Identification

- **Name:** `resume_processing_steps`
- **Type:** Table

## 2. Purpose

Stores resume processing step records belonging to a processing run, including step identity, ordering and attempts, timing, input/output summaries, duration, memory and CPU performance measurements, metadata, and embedded error data.

## 3. Data Definition

| Name | Type | Constraints | Description |
| --- | --- | --- | --- |
| `step_id` | TEXT | Primary Key, Not Null | UUID identifying the processing step record. |
| `run_id` | TEXT | Foreign Key `resume_processing_runs.run_id`, Not Null, On Delete Cascade | Parent processing run record. |
| `step_name` | TEXT | Not Null | Name of the processing step. |
| `step_order` | INTEGER | Not Null | Execution order of the step within the run. |
| `attempt_number` | INTEGER | Not Null | Attempt number for the step. |
| `status` | TEXT | Not Null, Check (`RUNNING`, `SUCCESS`, `FAILED`, `VALIDATION_FAILED`, `PARTIAL_SUCCESS`, `SKIPPED`, `CANCELLED`, `TIMEOUT`) | Execution status of the step. |
| `started_at` | DATETIME | Not Null | Time the step started. |
| `completed_at` | DATETIME | Nullable | Time the step completed. |
| `duration_ms` | FLOAT | Nullable | Step duration in milliseconds. |
| `input` | JSON | Not Null | Summary of the step input. |
| `output` | JSON | Not Null | Summary of the step output. |
| `performance` | JSON | Not Null | Step-level duration, memory, and CPU performance measurements. |
| `error` | JSON | Nullable | Embedded error object for the step, or null when no step-level error is recorded. |
| `metadata` | JSON | Not Null | Additional step-specific metadata; the ORM attribute is `metadata_json`, mapped to the `metadata` column. |

Indexes:
- Index on `run_id`.
- Unique index on `(run_id, step_order, attempt_number)`.

## 4. Relationships

- Many `resume_processing_steps` records belong to one `resume_processing_runs` record.
- One `resume_processing_steps` record has zero or more `llm_logs` records; each `llm_logs` record references a step through nullable `llm_logs.processing_step_id` with `ON DELETE SET NULL`.
- `input.source_step_id`, when present, is an identifier reference and does not define a foreign-key relationship.

## 5. Validation

- `step_id` must be unique.
- `run_id` must reference an existing processing run.
- `status` must be one of `RUNNING`, `SUCCESS`, `FAILED`, `VALIDATION_FAILED`, `PARTIAL_SUCCESS`, `SKIPPED`, `CANCELLED`, or `TIMEOUT`.
- `(run_id, step_order, attempt_number)` must be unique.
- `step_order` and `attempt_number` must be positive integers.
- `started_at` must not be null.
- `completed_at`, when present, must not occur before `started_at`.
- `duration_ms`, when present, must be non-negative.
- `input`, `output`, `performance`, and `metadata` must contain valid JSON values matching their documented structures.
- `performance` may contain `duration_ms`, `start_memory_mb`, `peak_memory_mb`, `end_memory_mb`, `memory_delta_mb`, `cpu_avg_percent`, `cpu_peak_percent`, and `sample_count`; short-running operations may record `sample_count` of 0 with null CPU values.
- `error`, when present, must contain a valid JSON object conforming to the embedded processing error structure.

## 6. References

- [SQLite Database Overview](/app/database/docs/sqlite/overview.md)
- [Resume Processing Runs Table](/app/database/docs/sqlite/schemas/resume-processing-runs.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Error Data Model](/docs/data/error.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)
- [Persist Resume Processing Step Technical Process](/app/database/docs/system/database-adapter/processes/persist-resume-processing-step.md)
