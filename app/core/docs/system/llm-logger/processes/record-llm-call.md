# Record LLM Call Technical Process

## 1. Purpose

Build an LLM activity log record from a generation call and deliver it to the Logger Service.

## 2. Objective

Capture request, result, usage, performance, and error information for one generation call without changing call behavior.

## 3. Scope

- Receive a generation request and measurement.
- Receive a generation result or an exception.
- Build the LLM activity log record.
- Deliver the record to the Logger Service.

The process does not perform generation or persist records itself.

## 4. Rules & Constraints

- The process must run only for `generate_structured`.
- The process must split system and user messages into `system_prompt` and `prompt`.
- The process must leave all generation parameters null.
- The process must set response content, finish reason, and token usage from the generation result.
- The process must set the timeout status for timeout errors and failed status for all other errors.
- The process must re-raise any exception after logging.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B[Receive request and measurement]
    B --> C{Generation result available?}
    C -->|Yes| D[Build success record]
    C -->|Timeout error| E[Build timeout record]
    C -->|Other error| F[Build failed record]
    D --> G[Emit record]
    E --> G
    F --> G
    G --> H{Return or re-raise original outcome}
    H --> I([End])
````

### Steps

1. Receive the generation request, measurement, and outcome.
2. Extract the system prompt and user prompt from messages.
3. Build request, response, usage, performance, and error values.
4. Determine status from the outcome.
5. Emit the record through the Logger Service.
6. Return the result or re-raise the original exception.

## 6. Modules

- `app/core/services/llm/logger.py` — Builds and emits LLM activity log records.
- `app/core/services/llm/log_models.py` — Defines LLM activity log records.
- `app/core/services/logger/performance.py` — Defines performance measurements.
- `app/core/services/logger/service.py` — Delivers the record to sinks.

## 7. Data

- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| REC-001 | A successful generation call. | The call completes. | A success record is emitted and the result is returned. |
| REC-002 | A timeout error. | The call fails. | A timeout record is emitted and the error is re-raised. |
| REC-003 | A non-timeout error. | The call fails. | A failed record is emitted and the error is re-raised. |
| REC-004 | System and user messages. | A record is built. | Prompts are split correctly and parameters are null. |

### 8.3 Test Coverage

Tests must verify record construction, classification, and unchanged call outcomes.

### 8.4 Test Organization

Tests reside under `tests/core/services/llm/`.

### 8.5 Test Dependencies

Use test doubles for the Logger Service and LLM port.

### 8.6 Testing Rules Compliance

Tests verify observable behavior, use test doubles only for external boundaries, and avoid implementation-detail assertions.

## 9. References

- [LLM Logger Technical System Specification](/app/core/docs/system/llm-logger/overview.md)
- [Record LLM Call Process](/docs/system/llm-logger/processes/record-llm-call.md)
