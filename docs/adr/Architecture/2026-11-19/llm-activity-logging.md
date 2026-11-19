# Log LLM Activities to the Database

## Date

2026-11-19

## Status

Accepted

## Category

architecture

## Context

Language-model calls are the only activities currently lacking an audit trail. The application needs to record the request, response, token usage, timing, memory use, and errors for language-model operations so results and failures can be reviewed later. These records must not include unrelated application activity.

## Decision

- Add an LLM Activity Log data model containing provider, model, operation, status, request details, response details, usage, timing, memory, error information, and creation time.
- Persist LLM activity logs in a dedicated SQLite table owned by the Database Adapter.
- Capture LLM activity at the LLM adapter boundary so the logger observes all language-model calls without changes to resume processing workflows.
- Record only structured generation calls. Availability checks and model listings are not logged because the agreed data model requires a model and prompt.
- Capture token usage and finish reason from the language-model response, and sample memory and duration around each call.
- Store generation parameters as null; the application does not currently supply temperature, top_p, top_k, num_ctx, or max_tokens.
- Map timeouts to a distinct status and all other failures to a failed status.
- Preserve existing call behavior: logging must not change requests, responses, or propagated errors.

## Consequences

- A new database table and migration are required.
- The LLM adapter boundary gains a logging wrapper and the Core LLM port gains a structured result carrying usage and finish reason.
- Reviewers can query LLM activity independently of other application data.
- Memory sampling adds small runtime overhead to language-model calls only.
