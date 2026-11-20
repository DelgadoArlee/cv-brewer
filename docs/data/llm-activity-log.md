# LLM Activity Log Data Model

## 1. Description

This document defines the data model for a single LLM activity log record. The model represents one structured generation call, including its optional processing step reference, request, response, token usage, performance measurements, error details, and creation time. It is used to review language-model results and failures independently of other application activity.

## 2. JSON Model

````json
{
  "id": "9f8f5b6e-3a0c-4a0e-9b9a-6d4a5b6a2b11",
  "processing_step_id": null,
  "provider": "ollama",
  "model": "llama3.2",
  "operation": "generate_structured",
  "status": "SUCCESS",
  "request": {
    "system_prompt": "You extract structured resume data.",
    "prompt": "Extract resume details from the following text.",
    "parameters": {
      "temperature": null,
      "top_p": null,
      "top_k": null,
      "num_ctx": null,
      "max_tokens": null
    }
  },
  "response": {
    "content": "{\"summary\": \"Example\"}",
    "finish_reason": "stop"
  },
  "usage": {
    "input_tokens": 128,
    "output_tokens": 42,
    "total_tokens": 170
  },
  "performance": {
    "started_at": "2026-11-19T10:15:00.000000",
    "completed_at": "2026-11-19T10:15:02.500000",
    "duration_ms": 2500.0,
    "start_memory_mb": 1.0,
    "peak_memory_mb": 1.5,
    "end_memory_mb": 1.2,
    "memory_delta_mb": 0.2,
    "cpu_avg_percent": 4.5,
    "cpu_peak_percent": 9.0,
    "sample_count": 3
  },
  "error": {
    "type": null,
    "message": null
  },
  "created_at": "2026-11-19T10:15:02.500000"
}
````

## 3. Data Fields

### Log Root Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| id | string | Yes | No | Unique identifier for the log record. | UUID format |
| processing_step_id | string | No | Yes | Identifier of the processing step during which the call was recorded. | UUID format when present; nullable reference to a [Resume Processing Step](/docs/data/resume-processing-step.md); indexed |
| provider | string | Yes | No | LLM provider name. | Non-empty |
| model | string | Yes | No | Model used for the call. | Non-empty |
| operation | string | Yes | No | LLM operation that was performed. | `generate_structured` |
| status | string | Yes | No | Outcome of the call. | `SUCCESS`, `FAILED`, or `TIMEOUT` |
| request | object | Yes | No | Request details for the call. | See Request Object |
| response | object | Yes | No | Response details for the call. | See Response Object |
| usage | object | Yes | No | Token usage reported by the provider. | See Usage Object |
| performance | object | Yes | No | Duration, memory, and CPU measurements. | See Performance Object |
| error | object | Yes | No | Error details when the call failed. | See Error Object |
| created_at | datetime | Yes | No | Time the record was created. | ISO 8601 timestamp |

### Request Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| system_prompt | string | No | Yes | System prompt supplied to the model. | Null when no system message exists |
| prompt | string | Yes | No | User prompt supplied to the model. | Non-empty |
| parameters | object | Yes | No | Generation parameters used for the call. | See Parameters Object |

### Parameters Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| temperature | number | No | Yes | Sampling temperature. | Null until supplied by the application |
| top_p | number | No | Yes | Nucleus sampling value. | Null until supplied by the application |
| top_k | integer | No | Yes | Top-k sampling value. | Null until supplied by the application |
| num_ctx | integer | No | Yes | Context window size. | Null until supplied by the application |
| max_tokens | integer | No | Yes | Maximum output tokens. | Null until supplied by the application |

### Response Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| content | string | No | Yes | Response content returned by the model. | Null when no response was produced |
| finish_reason | string | No | Yes | Reason the model stopped generating. | Null when unavailable |

### Usage Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| input_tokens | integer | No | Yes | Number of input tokens. | Non-negative when present |
| output_tokens | integer | No | Yes | Number of output tokens. | Non-negative when present |
| total_tokens | integer | No | Yes | Total tokens reported by the provider. | Non-negative when present |

### Performance Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| started_at | datetime | Yes | No | Time the call began. | ISO 8601 timestamp |
| completed_at | datetime | No | Yes | Time the call completed. | Null when measurement could not complete |
| duration_ms | number | No | Yes | Elapsed time in milliseconds. | Non-negative when present |
| start_memory_mb | number | No | Yes | Process memory before the call, in megabytes. | Non-negative when present |
| peak_memory_mb | number | No | Yes | Peak process memory during the call, in megabytes. | Non-negative when present |
| end_memory_mb | number | No | Yes | Process memory after the call, in megabytes. | Non-negative when present |
| memory_delta_mb | number | No | Yes | Difference between end and start process memory, in megabytes. | May be negative |
| cpu_avg_percent | number | No | Yes | Average process CPU usage during the call. | Null when no samples were collected |
| cpu_peak_percent | number | No | Yes | Peak process CPU usage during the call. | Null when no samples were collected |
| sample_count | integer | Yes | No | Number of performance samples collected during the call. | Non-negative integer; may be zero for short-running operations |

### Error Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| type | string | No | Yes | Error type or category. | Null on success |
| message | string | No | Yes | Error message. | Null on success |

## 4. Validation

- `status` must be one of `SUCCESS`, `FAILED`, or `TIMEOUT`.
- `processing_step_id`, when present, must identify a processing step; one step can have many LLM logs, and one LLM log can reference zero or one step.
- A successful record must contain response content and must not contain error details.
- A failed or timed-out record must contain error details and should not contain response content.
- `sample_count` may be zero for short-running operations, in which case `cpu_avg_percent` and `cpu_peak_percent` are null.
- Generation parameter fields must be null until the application supplies them.
- `created_at` must not be null.

## 5. References

- [LLM Activity Logging Decision](/docs/adr/Architecture/2026-11-19/llm-activity-logging.md)
- [LLM Logger System Overview](/docs/system/llm-logger/overview.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [LLM Logs Table Schema](/app/database/docs/sqlite/schemas/llm-logs.md)
