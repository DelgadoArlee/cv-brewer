# LLM Logger Technical System Specification

## 1. Purpose

Defines the LLM-specific logging implementation in Core that builds activity log records from generation calls and hands them to the generic Logger Service for persistence.

## 2. Objective

- Define LLM activity log records across Core and Database.
- Build records from generation requests, results, and errors.
- Classify timeout and failure outcomes.
- Provide a repository contract for persistence and querying.

## 3. Scope

### In Scope

- `app/core/services/llm/` logging records, logger, and repository contract.
- Generation result and usage records on the LLM port.
- Classification and construction of LLM activity log records.

### Out of Scope

- Capturing memory and duration mechanics, owned by the generic Logger Service.
- Provider-specific response parsing.
- Database implementation and display of records.

## 4. Rules & Constraints

- Only `generate_structured` calls may produce records.
- The provider and model must be supplied by the caller.
- Generation parameters must be recorded as null.
- A successful call must produce the `SUCCESS` status; a timeout error must produce `TIMEOUT`; any other error must produce `FAILED`.
- A log record may carry an optional `processing_step_id` supplied by the caller.
- The logger must not alter the observed call's request, response, or exception.

## 5. Process

| Process | Description | Specification |
| --- | --- | --- |
| Record LLM Call | Builds an activity log record from a generation call and delivers it. | [Record LLM Call](/app/core/docs/system/llm-logger/processes/record-llm-call.md) |

## 6. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| Logger Service | Internal system | Delivers the constructed log record to sinks. |
| LLM Adapter | Internal system | Supplies generation results and provider-specific usage data. |
| LLM Log Repository | Internal interface | Persists and lists LLM activity log records. |

## 7. Test Cases

| Test Case ID | Scenario | Expected Result | Related Rule |
| --- | --- | --- | --- |
| LLM-LOG-001 | A successful generation call. | A `SUCCESS` record with response, usage, and performance data is emitted. | Success rule |
| LLM-LOG-002 | A timed-out generation call. | A `TIMEOUT` record with error details is emitted. | Timeout rule |
| LLM-LOG-003 | A failed generation call. | A `FAILED` record with error details is emitted. | Failure rule |
| LLM-LOG-004 | A generation call with system and user messages. | Prompts are split into system prompt and prompt. | Request rule |
| LLM-LOG-005 | Generation parameters. | All parameter fields are null. | Parameter rule |

## 8. Architecture Decision Log

| ADR | Decision Summary |
| --- | --- |
| [Log LLM activities to the database](/docs/adr/Architecture/2026-11-19/llm-activity-logging.md) | Record LLM generation calls in a dedicated table. |
| [Establish the logger service package](/app/core/docs/adr/11-19-26/logger-service-package.md) | Keep LLM-specific log records in the LLM service package. |

## 9. Data

- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)

## 10. References

- [LLM Logger System Overview](/docs/system/llm-logger/overview.md)
- [Record LLM Call Technical Process](/app/core/docs/system/llm-logger/processes/record-llm-call.md)
- [Core Component Technical Specification](/app/core/docs/technical-specification.md)
