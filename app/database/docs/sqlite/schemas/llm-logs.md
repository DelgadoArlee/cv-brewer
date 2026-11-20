# LLM Logs Table Schema

## 1. Database Object Identification

- **Name:** `llm_logs`
- **Type:** Table

## 2. Purpose

Stores LLM activity log records for structured generation calls, including request details, an optional processing step reference, response details, token usage, performance measurements, and errors.

## 3. Data Definition

| Name | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | TEXT | Primary Key, Not Null | UUID identifying the log record. |
| `provider` | TEXT | Not Null | LLM provider name. |
| `model` | TEXT | Not Null | Model used for the call. |
| `operation` | TEXT | Not Null | LLM operation that was performed. |
| `processing_step_id` | TEXT | Nullable, Foreign Key `resume_processing_steps.step_id`, On Delete Set Null, Indexed | Processing step associated with the call, or null when no step is recorded. |
| `status` | TEXT | Not Null, Check (`SUCCESS`, `FAILED`, `TIMEOUT`) | Outcome of the call. |
| `system_prompt` | TEXT | Nullable | System prompt supplied to the model. |
| `prompt` | TEXT | Not Null | User prompt supplied to the model. |
| `parameters` | JSON | Not Null | Generation parameters; all fields are currently null. |
| `response_content` | TEXT | Nullable | Response content returned by the model. |
| `finish_reason` | TEXT | Nullable | Reason the model stopped generating. |
| `input_tokens` | INTEGER | Nullable | Number of input tokens. |
| `output_tokens` | INTEGER | Nullable | Number of output tokens. |
| `total_tokens` | INTEGER | Nullable | Total tokens reported by the provider. |
| `started_at` | DATETIME | Not Null | Time the call began. |
| `completed_at` | DATETIME | Nullable | Time the call completed. |
| `duration_ms` | FLOAT | Nullable | Elapsed time in milliseconds. |
| `start_memory_mb` | FLOAT | Nullable | Process memory in megabytes at the start of the call. |
| `peak_memory_mb` | FLOAT | Nullable | Peak process memory in megabytes during the call. |
| `end_memory_mb` | FLOAT | Nullable | Process memory in megabytes at the end of the call. |
| `memory_delta_mb` | FLOAT | Nullable | Difference between end and start memory in megabytes. |
| `cpu_avg_percent` | FLOAT | Nullable | Average process CPU utilization during the call. |
| `cpu_peak_percent` | FLOAT | Nullable | Peak process CPU utilization during the call. |
| `sample_count` | INTEGER | Not Null, Default `0` | Number of CPU samples collected during the call. |
| `error_type` | TEXT | Nullable | Error type or category. |
| `error_message` | TEXT | Nullable | Error message. |
| `created_at` | DATETIME | Not Null | Time the record was created. |

Indexes:
- Index on `processing_step_id`.
- Index on `created_at`.

## 4. Relationships

- Each `llm_logs` record references zero or one `resume_processing_steps` record through nullable `processing_step_id` with `ON DELETE SET NULL`.
- One `resume_processing_steps` record has zero or more `llm_logs` records.

## 5. Validation

- `status` must be one of `SUCCESS`, `FAILED`, or `TIMEOUT`.
- `processing_step_id`, when present, must reference an existing processing step.
- `prompt` must not be null.
- Generation parameter fields inside `parameters` are null until the application supplies them.
- Nullable measurement and error columns may be null when no value is available.
- Short-running operations may record `sample_count` of 0 with null CPU values.

## 6. References

- [SQLite Database Overview](/app/database/docs/sqlite/overview.md)
- [Resume Processing Steps Table](/app/database/docs/sqlite/schemas/resume-processing-steps.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)
- [Persist LLM Log Technical Process](/app/database/docs/system/database-adapter/processes/persist-llm-log.md)
