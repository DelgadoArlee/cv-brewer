# Logger Service Technical System Specification

## 1. Purpose

Defines the generic logging engine in Core that accepts structured log records, measures activity performance, and delivers records to configured sinks.

## 2. Objective

- Define a common log record and status representation.
- Provide reusable duration and memory measurement.
- Deliver records to every configured sink.
- Keep destination-specific behavior outside Core.

## 3. Scope

### In Scope

- `app/core/services/logger/` package.
- Generic log record, status, error, and performance values.
- Performance measurement helper.
- Sink contract and logging service operations.

### Out of Scope

- LLM-specific request, response, and usage records.
- Database, file, or console sink implementations.
- Log display and querying.
- Selection of application activities to log.

## 4. Rules & Constraints

- The service must accept a generic log record and forward it unchanged to each configured sink.
- The service must not import database or LLM adapter implementations.
- Sinks must be supplied through constructor injection.
- Performance measurement must capture start time, completion time, duration, and memory before, after, peak, and delta.
- The service must not create records for general application events.

## 5. Process

| Process | Description | Specification |
| --- | --- | --- |
| Emit Log Entry | Delivers a log record to every configured sink. | [Emit Log Entry](/app/core/docs/system/logger-service/processes/emit-log-entry.md) |

## 6. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `LogSink` | Internal interface | Destination contract implemented outside the logging package. |

## 7. Test Cases

| Test Case ID | Scenario | Expected Result | Related Rule |
| --- | --- | --- | --- |
| LOG-SVC-001 | Emit a record with one sink. | The sink receives the unchanged record. | Delivery rule |
| LOG-SVC-002 | Emit a record with several sinks. | Every sink receives the unchanged record. | Delivery rule |
| LOG-SVC-003 | Emit a record with no sinks. | The operation completes without error. | No-destination rule |
| LOG-SVC-004 | A sink fails during delivery. | The failure is reported to the caller. | Failure rule |
| LOG-SVC-005 | Measure an activity. | Timing and memory values are captured. | Measurement rule |

## 8. Architecture Decision Log

| ADR | Decision Summary |
| --- | --- |
| [Add a Core-owned Logger Service](/docs/adr/Architecture/2026-11-19/core-logger-service.md) | Define generic log records and a sink contract in Core. |
| [Establish the logger service package](/app/core/docs/adr/11-19-26/logger-service-package.md) | Place generic logging in `app/core/services/logger/`. |

## 9. References

- [Logger Service System Overview](/docs/system/logger-service/overview.md)
- [Core Component Technical Specification](/app/core/docs/technical-specification.md)
- [Emit Log Entry Technical Process](/app/core/docs/system/logger-service/processes/emit-log-entry.md)
