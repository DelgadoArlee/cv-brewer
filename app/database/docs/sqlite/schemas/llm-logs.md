# LLM Logs Table Schema

## 1. Database Object Identification

- **Name:** `llm_logs`
- **Type:** Table

## 2. Purpose

Stores LLM activity log records for structured generation calls, including request details, response details, token usage, performance measurements, and errors.

## 3. Data Definition

| Name | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | TEXT | Primary Key, Not Null | UUID identifying the log record. |
| `provider` | TEXT | Not Null | LLM provider name. |
| `model` | TEXT | Not Null | Model used for the call. |
| `operation` | TEXT | Not Null | LLM operation that was performed. |
| `status` | TEXT | Not Null, Check (`success`, `failed`, `timeout`) | Outcome of the call. |
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
| `memory_before_bytes` | INTEGER | Nullable | Tracked memory before the call. |
| `memory_after_bytes` | INTEGER | Nullable | Tracked memory after the call. |
| `memory_peak_bytes` | INTEGER | Nullable | Peak tracked memory during the call. |
| `memory_delta_bytes` | INTEGER | Nullable | Difference between memory after and before. |
| `error_type` | TEXT | Nullable | Error type or category. |
| `error_message` | TEXT | Nullable | Error message. |
| `created_at` | DATETIME | Not Null | Time the record was created. |

Indexes:
- Index on `created_at`.

## 4. Relationships

- The table has no foreign-key relationship to other tables.

## 5. Validation

- `status` must be one of `success`, `failed`, or `timeout`.
- `prompt` must not be null.
- Generation parameter fields inside `parameters` are null until the application supplies them.
- Nullable measurement and error columns may be null when no value is available.

## 6. References

- [SQLite Database Overview](/app/database/docs/sqlite/overview.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)
- [Persist LLM Log Technical Process](/app/database/docs/system/database-adapter/processes/persist-llm-log.md)
