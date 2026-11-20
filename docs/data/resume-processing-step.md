# Resume Processing Step Data Model

## 1. Description

This document defines the data model for a resume processing step in CVBrewer. The model represents one recorded step within a resume processing run, including step identity, execution order and attempt, timing, input and output summaries, performance measurements, step metadata, and embedded error data. LLM activity logs may reference the step during which they were recorded. Processing steps belong to a processing run in a one-to-many relationship.

## 2. JSON Model

````json
{
  "step_id": "uuid",
  "run_id": "uuid",
  "step_name": "parsing",
  "step_order": 6,
  "attempt_number": 1,
  "status": "SUCCESS",
  "started_at": "2026-11-19T10:00:04Z",
  "completed_at": "2026-11-19T10:00:05Z",
  "duration_ms": 1000.0,
  "input": {
    "type": "extracted_text",
    "source_step_id": "previous-step-uuid",
    "size_bytes": 12500,
    "hash": "sha256:...",
    "metadata": {
      "page_count": 3,
      "character_count": 12000
    },
    "snapshot": null
  },
  "output": {
    "type": "resume_data",
    "size_bytes": 8500,
    "hash": "sha256:...",
    "metadata": {
      "fields_extracted": 35,
      "missing_fields": 2
    },
    "snapshot": null
  },
  "performance": {
    "duration_ms": 1000.0,
    "start_memory_mb": 180.0,
    "peak_memory_mb": 230.0,
    "end_memory_mb": 210.0,
    "memory_delta_mb": 30.0,
    "cpu_avg_percent": 8.0,
    "cpu_peak_percent": 20.0,
    "sample_count": 1
  },
  "error": null,
  "metadata": {}
}
````

## 3. Data Fields

### Processing Step Root Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| step_id | string | Yes | No | Unique identifier for the processing step record. | UUID format |
| run_id | string | Yes | No | Identifier of the processing run that owns this step. | UUID format; references a [Resume Processing Run](/docs/data/resume-processing-run.md) |
| step_name | string | Yes | No | Name of the processing step. | Non-empty string |
| step_order | integer | Yes | No | Execution order of the step within the run. | Positive integer |
| attempt_number | integer | Yes | No | Attempt number for the step. | Positive integer |
| status | string | Yes | No | Execution status of the step. | One of `RUNNING`, `SUCCESS`, `FAILED`, `VALIDATION_FAILED`, `PARTIAL_SUCCESS`, `SKIPPED`, `CANCELLED`, `TIMEOUT` |
| started_at | datetime | Yes | No | Time the step started. | ISO 8601 timestamp |
| completed_at | datetime | No | Yes | Time the step completed. | ISO 8601 timestamp when present |
| duration_ms | number | No | Yes | Step duration in milliseconds. | Non-negative when present |
| input | object | Yes | No | Summary of the step input. | See Input Object |
| output | object | Yes | No | Summary of the step output. | See Output Object |
| performance | object | Yes | No | Step-level performance measurements. | See Performance Object |
| error | object | No | Yes | Embedded error information for the step. | `null` when no step-level error is recorded; see [Error Data Model](/docs/data/error.md) |
| metadata | object | Yes | No | Additional step-specific metadata. | May be an empty object |

### Input Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| type | string | Yes | No | Type of input processed by the step. | Non-empty string |
| source_step_id | string | No | Yes | Identifier of a prior step that produced this input. | UUID format when present; reference only |
| size_bytes | integer | No | Yes | Size of the input in bytes. | Non-negative when present |
| hash | string | No | Yes | Hash or fingerprint of the input. | Null when unavailable |
| metadata | object | Yes | No | Additional input metadata. | May be an empty object |
| snapshot | object | No | Yes | Optional captured snapshot of input content or structure. | Null when not captured; structure may vary |

### Output Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| type | string | Yes | No | Type of output produced by the step. | Non-empty string |
| size_bytes | integer | No | Yes | Size of the output in bytes. | Non-negative when present |
| hash | string | No | Yes | Hash or fingerprint of the output. | Null when unavailable |
| metadata | object | Yes | No | Additional output metadata. | May be an empty object |
| snapshot | object | No | Yes | Optional captured snapshot of output content or structure. | Null when not captured; structure may vary |

### Performance Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| duration_ms | number | No | Yes | Step duration in milliseconds. | Non-negative when present |
| start_memory_mb | number | No | Yes | Process memory before the step, in megabytes. | Non-negative when present |
| peak_memory_mb | number | No | Yes | Peak process memory during the step, in megabytes. | Non-negative when present |
| end_memory_mb | number | No | Yes | Process memory after the step, in megabytes. | Non-negative when present |
| memory_delta_mb | number | No | Yes | Difference between end and start process memory, in megabytes. | May be negative |
| cpu_avg_percent | number | No | Yes | Average process CPU usage during the step. | Null when no samples were collected |
| cpu_peak_percent | number | No | Yes | Peak process CPU usage during the step. | Null when no samples were collected |
| sample_count | integer | Yes | No | Number of performance samples collected during the step. | Non-negative integer; may be zero for short-running operations |

## 4. Validation

- `step_id` must be unique.
- `run_id` must reference an existing processing run record; deleting a run deletes its steps.
- Each processing step belongs to exactly one processing run, and a processing run may have multiple processing steps.
- `step_name` must be one of `file_type_validation`, `metadata_extraction`, `deduplication`, `pdf_validation`, `content_extraction`, `parsing`, `schema_validation`, or `storage`.
- `status`, when finalized, must be one of `SUCCESS`, `FAILED`, `VALIDATION_FAILED`, `PARTIAL_SUCCESS`, `SKIPPED`, `CANCELLED`, or `TIMEOUT`; a step in progress has status `RUNNING`.
- `step_order` and `attempt_number` must be positive integers.
- `started_at` must not be null.
- `completed_at`, when present, must not occur before `started_at`.
- `duration_ms`, when present, must be non-negative.
- `input`, `output`, `performance`, and `metadata` must be present.
- `sample_count` may be zero for short-running operations, in which case `cpu_avg_percent` and `cpu_peak_percent` are null.
- `source_step_id`, when present, is an identifier reference and must identify a related step when such a relationship is recorded.
- An LLM activity log may reference this step; one step can have many LLM logs, and one LLM log can reference zero or one step.
- `error` must be `null` when no step-level error is recorded; when present, it must conform to the [Error Data Model](/docs/data/error.md).

## 5. References

- [Error Data Model](/docs/data/error.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)
- [Resume Processing System Overview](/docs/system/resume-processing/overview.md)
- [Resume Processing Process](/docs/system/resume-processing/processes/resume-processing.md)
