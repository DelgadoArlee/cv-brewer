# Logger Service System Overview

## 1. Purpose

The Logger Service records structured activity information and routes it to configured destinations. It exists so applications can capture consistent log records without each caller writing its own logging and delivery logic.

## 2. Objectives

- Define a common log record for structured activity information.
- Route each log record to one or more configured destinations.
- Measure activity duration and memory use consistently.
- Allow new destinations to be added without changing callers.
- Support LLM logging as a specialized use without recording unrelated application events.

## 3. Scope

### In Scope

- Generic log records, statuses, error details, and performance details.
- Measurement of duration and memory use around a logged activity.
- Delivery of log records to configured destinations.
- A destination contract implemented outside the Logger Service.

### Out of Scope

- Defining LLM-specific request, response, or usage records.
- Choosing which application activities are logged.
- Database connections, queries, and schema management.
- Displaying logs to users.
- General application event, PDF processing, database operation, or non-LLM performance logging.

## 4. Workflow

Callers build a log record, measure the activity, and submit the record to the Logger Service. The service forwards the record to every configured destination.

See the [Emit Log Entry Process](/docs/system/logger-service/processes/emit-log-entry.md).

## 5. Constraints

- The Logger Service must not depend on a specific destination implementation.
- The Logger Service must not interpret the contents of a log record beyond delivery.
- Destinations must be supplied to the service by the application composition root.
- Logging failures must be reported through standard logging and must not interrupt the originating activity.

## 6. References

- [Core-owned Logger Service Decision](/docs/adr/Architecture/2026-11-19/core-logger-service.md)
- [Logger Service Technical System Specification](/app/core/docs/system/logger-service/overview.md)
