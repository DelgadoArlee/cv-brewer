# LLM Logger System Overview

## 1. Purpose

The LLM Logger records LLM generation calls so their requests, results, token usage, performance, and errors can be reviewed. It uses the Logger Service to deliver records and the Database Adapter to store them.

## 2. Objectives

- Record only LLM generation activities.
- Capture the model, provider, prompt content, response content, and finish reason.
- Capture token usage, duration, and memory use for each call.
- Distinguish successful, failed, and timed-out calls.
- Persist each log record so it can be queried later.

## 3. Scope

### In Scope

- LLM-specific log records.
- Measurement and classification of a generation call outcome.
- Persistence of LLM log records through a Core-owned repository contract.
- Listing persisted LLM log records for review.

### Out of Scope

- General application event logging.
- PDF processing, resume parsing, schema validation, and non-LLM performance logging.
- Database connection management and migration implementation.
- User-interface rendering of logs.
- Invoking language models.

## 4. Workflow

A generation call is measured and classified. Its request, response, usage, performance, and error details form an LLM activity log record that is delivered to the Logger Service and persisted by a destination.

See the [Record LLM Call Process](/docs/system/llm-logger/processes/record-llm-call.md) and the [Persist LLM Log Process](/docs/system/database-service/processes/persist-llm-log.md).

## 5. Data Management

The system uses the [LLM Activity Log Data Model](/docs/data/llm-activity-log.md).

## 6. Error Handling

- A timed-out call must be recorded with the timeout status.
- Any other unsuccessful call must be recorded with the failed status and error details.
- Logging must not change the request, response, or error returned to the original caller.

## 7. References

- [LLM Activity Logging Decision](/docs/adr/Architecture/2026-11-19/llm-activity-logging.md)
- [LLM Logger Technical System Specification](../../app/core/docs/system/llm-logger/overview.md)
- [Logger Service System Overview](/docs/system/logger-service/overview.md)
