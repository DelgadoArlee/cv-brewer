# Resume Processing Runs Table Schema

## 1. Database Object Identification

- **Name:** `resume_processing_runs`
- **Type:** Table

## 2. Purpose

Stores resume processing run records, including run identity, outcome, timing, step summary, performance measurements, resume identifier references, and embedded error data.

## 3. Data Definition

| Name | Type | Constraints | Description |
| --- | --- | --- | --- |
| `run_id` | TEXT | Primary Key, Not Null | UUID identifying the processing run. |
| `process_name` | TEXT | Not Null | Name of the executed process. |
| `process_version` | TEXT | Not Null | Version identifier of the executed process definition. |
| `status` | TEXT | Not Null, Check (`RUNNING`, `SUCCESS`, `FAILED`, `VALIDATION_FAILED`, `PARTIAL_SUCCESS`, `SKIPPED`, `CANCELLED`, `TIMEOUT`) | Execution status of the run. |
| `result` | TEXT | Nullable | Processing result of the run. |
| `resume_id` | TEXT | Nullable | Database identifier of the saved parsed resume referenced by the run; stored without a foreign-key relationship. |
| `matched_resume_id` | TEXT | Nullable | Database identifier of an existing matched resume referenced by the run; stored without a foreign-key relationship. |
| `started_at` | DATETIME | Not Null | Time the run started. |
| `completed_at` | DATETIME | Nullable | Time the run completed. |
| `duration_ms` | FLOAT | Nullable | Total run duration in milliseconds. |
| `summary` | JSON | Not Null | Aggregated step outcome counts for the run. |
| `performance` | JSON | Not Null | Run-level duration, memory, and CPU performance measurements. |
| `error` | JSON | Nullable | Embedded error object for the run, or null when no run-level error is recorded. |

Indexes:
- Index on `started_at`.
- Index on `resume_id`.

## 4. Relationships

- One `resume_processing_runs` record has zero or more `resume_processing_steps` records.
- `resume_id` and `matched_resume_id` are identifier references only and do not define foreign-key relationships to `resumes` or other tables.

## 5. Validation

- `run_id` must be unique.
- `status` must be one of `RUNNING`, `SUCCESS`, `FAILED`, `VALIDATION_FAILED`, `PARTIAL_SUCCESS`, `SKIPPED`, `CANCELLED`, or `TIMEOUT`.
- `resume_id` and `matched_resume_id`, when present, must not be enforced as foreign keys.
- `started_at` must not be null.
- `completed_at`, when present, must not occur before `started_at`.
- `duration_ms`, when present, must be non-negative.
- `summary` and `performance` must contain valid JSON objects.
- `performance` may contain `duration_ms`, `start_memory_mb`, `peak_memory_mb`, `end_memory_mb`, `memory_delta_mb`, `cpu_avg_percent`, `cpu_peak_percent`, and `sample_count`; short-running operations may record `sample_count` of 0 with null CPU values.
- `error`, when present, must contain a valid JSON object conforming to the embedded processing error structure.

## 6. References

- [SQLite Database Overview](/app/database/docs/sqlite/overview.md)
- [Resume Processing Step Table](/app/database/docs/sqlite/schemas/resume-processing-steps.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Error Data Model](/docs/data/error.md)
- [Persist Resume Processing Run Technical Process](/app/database/docs/system/database-adapter/processes/persist-resume-processing-run.md)
