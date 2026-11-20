# Resume Processing Run Data Model

## 1. Description

This document defines the data model for a resume processing run in CVBrewer. The model represents one execution of the resume processing workflow, including its identity, outcome, timing, step summary, performance measurements, and embedded error data. A processing run records processing activity for a resume file and may reference the stored parsed resume record by database identifier without creating a database relationship to that record.

## 2. JSON Model

````json
{
  "run_id": "uuid",
  "process_name": "resume_processing",
  "process_version": "1.0",
  "status": "SUCCESS",
  "result": "stored",
  "resume_id": "uuid",
  "matched_resume_id": null,
  "started_at": "2026-11-19T10:00:00Z",
  "completed_at": "2026-11-19T10:00:08Z",
  "duration_ms": 8000.0,
  "summary": {
    "total_steps": 8,
    "completed_steps": 8,
    "failed_steps": 0,
    "skipped_steps": 0
  },
  "performance": {
    "duration_ms": 8000.0,
    "start_memory_mb": 120.0,
    "peak_memory_mb": 450.0,
    "end_memory_mb": 180.0,
    "memory_delta_mb": 60.0,
    "cpu_avg_percent": 12.5,
    "cpu_peak_percent": 35.0,
    "sample_count": 8
  },
  "error": null
}
````

## 3. Data Fields

### Processing Run Root Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| run_id | string | Yes | No | Unique identifier for the processing run. | UUID format |
| process_name | string | Yes | No | Name of the executed process. | Non-empty string; `resume_processing` for resume processing runs |
| process_version | string | Yes | No | Version identifier of the executed process definition. | Non-empty string |
| status | string | Yes | No | Execution status of the run. | One of `RUNNING`, `SUCCESS`, `FAILED`, `VALIDATION_FAILED`, `PARTIAL_SUCCESS`, `SKIPPED`, `CANCELLED`, `TIMEOUT` |
| result | string | No | Yes | Processing result of the run after finalization. | Non-empty string when present |
| resume_id | string | No | Yes | Database identifier of the saved parsed resume referenced by this run. | UUID format when present; reference only, no database relationship |
| matched_resume_id | string | No | Yes | Database identifier of an existing matched resume associated with the run outcome. | UUID format when present; reference only, no database relationship |
| started_at | datetime | Yes | No | Time the run started. | ISO 8601 timestamp |
| completed_at | datetime | No | Yes | Time the run completed. | ISO 8601 timestamp when present |
| duration_ms | number | No | Yes | Total run duration in milliseconds. | Non-negative when present |
| summary | object | Yes | No | Aggregated step outcome counts for the run. | See Summary Object |
| performance | object | Yes | No | Run-level performance measurements. | See Performance Object |
| error | object | No | Yes | Embedded error information for the run. | `null` when no run-level error is recorded; see [Error Data Model](/docs/data/error.md) |

### Summary Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| total_steps | integer | Yes | No | Total number of processing steps recorded for the run. | Non-negative integer |
| completed_steps | integer | Yes | No | Number of steps completed successfully. | Non-negative integer |
| failed_steps | integer | Yes | No | Number of steps that failed. | Non-negative integer |
| skipped_steps | integer | Yes | No | Number of steps that were skipped. | Non-negative integer |

### Performance Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| duration_ms | number | No | Yes | Run duration in milliseconds. | Non-negative when present |
| start_memory_mb | number | No | Yes | Process memory at run start, in megabytes. | Non-negative when present |
| peak_memory_mb | number | No | Yes | Peak process memory during the run, in megabytes. | Non-negative when present |
| end_memory_mb | number | No | Yes | Process memory at run end, in megabytes. | Non-negative when present |
| memory_delta_mb | number | No | Yes | Difference between end and start process memory, in megabytes. | May be negative |
| cpu_avg_percent | number | No | Yes | Average process CPU usage during the run. | Null when no samples were collected |
| cpu_peak_percent | number | No | Yes | Peak process CPU usage during the run. | Null when no samples were collected |
| sample_count | integer | Yes | No | Number of performance samples collected during the run. | Non-negative integer; may be zero for short-running operations |

## 4. Validation

- `run_id` must be unique.
- `status`, when finalized, must be one of `SUCCESS`, `FAILED`, `VALIDATION_FAILED`, `PARTIAL_SUCCESS`, `SKIPPED`, `CANCELLED`, or `TIMEOUT`; a run in progress has status `RUNNING`.
- `started_at` must not be null.
- `completed_at`, when present, must not occur before `started_at`.
- `duration_ms`, when present, must be non-negative.
- `summary` and `performance` must be present.
- `sample_count` may be zero for short-running operations, in which case `cpu_avg_percent` and `cpu_peak_percent` are null.
- `summary` counts must be non-negative and consistent with the recorded processing steps.
- `resume_id` and `matched_resume_id`, when present, are identifier references only and must not imply a database relationship.
- `error` must be `null` when no run-level error is recorded; when present, it must conform to the [Error Data Model](/docs/data/error.md).
- A processing run may have zero or more associated [Resume Processing Step](/docs/data/resume-processing-step.md) records; deleting a run deletes its steps.

## 5. References

- [Error Data Model](/docs/data/error.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [User Resume Data Model](/docs/data/user-resume.md)
- [Resume Processing System Overview](/docs/system/resume-processing/overview.md)
- [Resume Processing Process](/docs/system/resume-processing/processes/resume-processing.md)
