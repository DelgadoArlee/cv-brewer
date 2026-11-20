# Error Data Model

## 1. Description

This document defines a general data model for embedded error information in CVBrewer. The model provides a consistent structure for capturing failure details in system-specific logs and records while allowing system-specific content in `details` and `raw`. It can be embedded in records such as [Resume Processing Run](/docs/data/resume-processing-run.md) and [Resume Processing Step](/docs/data/resume-processing-step.md) to preserve error information alongside recorded activity.

## 2. JSON Model

````json
{
  "code": "LLM_REQUEST_TIMEOUT",
  "type": "llm_error",
  "message": "LLM generation request timed out.",
  "details": {
    "model": "qwen3.5:9b",
    "timeout_seconds": 120
  },
  "raw": {
    "exception_class": "ReadTimeout",
    "exception_message": "Request timed out.",
    "exception_args": [
      "Request timed out."
    ],
    "traceback": "Full traceback...",
    "cause": null,
    "context": null
  },
  "occurred_at": "2026-11-19T10:00:05Z"
}
````

## 3. Data Fields

### Error Root Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| code | string | Yes | No | Machine-readable error code. | Non-empty string |
| type | string | Yes | No | Error category or classification. | Non-empty string |
| message | string | Yes | No | Human-readable error message. | Non-empty string |
| details | object | Yes | No | Structured, system-specific error details relevant to the failure. | See Details Object |
| raw | object | Yes | No | Raw exception and diagnostic details. | See Raw Object |
| occurred_at | datetime | Yes | No | Time the error occurred. | ISO 8601 timestamp |

### Details Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| * | any | No | Yes | System-specific detail fields. | Structure varies by system, `code`, and `type`; may be an empty object when no additional details are available |

### Raw Object

| Name | Type | Required | Nullable | Description | Constraints |
| --- | --- | --- | --- | --- | --- |
| exception_class | string | No | Yes | Name of the originating exception class. | Null when unavailable |
| exception_message | string | No | Yes | Original exception message. | Null when unavailable |
| exception_args | array | No | Yes | Original exception arguments. | Array values may vary by exception |
| traceback | string | No | Yes | Captured traceback text. | Null when unavailable |
| cause | object | No | Yes | Raw cause information for a chained exception. | Null when unavailable; structure may vary by system |
| context | object | No | Yes | Raw context information for a chained exception. | Null when unavailable; structure may vary by system |

## 4. Validation

- An embedded error must include `code`, `type`, `message`, `details`, `raw`, and `occurred_at`.
- `occurred_at` must be a valid ISO 8601 timestamp.
- `details` and `raw` must be objects; their internal fields may vary based on the system and failure source.
- `raw` must contain the traceback text for the originating exception.
- System-specific logs may define additional constraints on `code`, `type`, and the contents of `details` and `raw`.
- When a log record has no error, its embedded `error` value must be `null` where the record includes an `error` field.

## 5. References

- [Data Model Format Rules](/docs/rules/data.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
