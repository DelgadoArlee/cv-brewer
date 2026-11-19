# LLM Activity Log Data Model

## 1. Description

This document defines the data model for a single LLM activity log record. The model represents one structured generation call, including its request, response, token usage, performance measurements, error details, and creation time. It is used to review language-model results and failures independently of other application activity.

## 2. JSON Model

````json
{
  "id": "9f8f5b6e-3a0c-4a0e-9b9a-6d4a5b6a2b11",
  "provider": "ollama",
  "model": "llama3.2",
  "operation": "generate_structured",
  "status": "success",
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
    "memory_before_bytes": 1000000,
    "memory_after_bytes": 1200000,
    "memory_peak_bytes": 1500000,
    "memory_delta_bytes": 200000
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
| provider | string | Yes | No | LLM provider name. | Non-empty |
| model | string | Yes | No | Model used for the call. | Non-empty |
| operation | string | Yes | No | LLM operation that was performed. | `generate_structured` |
| status | string | Yes | No | Outcome of the call. | `success`, `failed`, or `timeout` |
| request | object | Yes | No | Request details for the call. | See Request Object |
| response | object | Yes | No | Response details for the call. | See Response Object |
| usage | object | Yes | No | Token usage reported by the provider. | See Usage Object |
| performance | object | Yes | No | Duration and memory measurements. | See Performance Object |
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
| memory_before_bytes | integer | No | Yes | Tracked memory before the call. | Non-negative when present |
| memory_after_bytes | integer | No | Yes | Tracked memory after the call. | Non-negative when present |
| memory_peak_bytes | integer | No | Yes | Peak tracked memory during the call. | Non-negative when present |
| memory_delta_bytes | integer | No | Yes | Difference between memory after and before. | May be negative |

### Error Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| type | string | No | Yes | Error type or category. | Null on success |
| message | string | No | Yes | Error message. | Null on success |

## 4. Validation

- `status` must be one of `success`, `failed`, or `timeout`.
- A successful record must contain response content and must not contain error details.
- A failed or timed-out record must contain error details and should not contain response content.
- Generation parameter fields must be null until the application supplies them.
- `created_at` must not be null.

## 5. References

- [LLM Activity Logging Decision](/docs/adr/Architecture/2026-11-19/llm-activity-logging.md)
- [LLM Logger System Overview](/docs/system/llm-logger/overview.md)
- [LLM Logs Table Schema](/app/database/docs/sqlite/schemas/llm-logs.md)
