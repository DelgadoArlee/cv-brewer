# Capture LLM Logs at the Adapter Boundary

## Date

2026-11-19

## Status

Accepted

## Context

The [Core-owned Logger Service](/docs/adr/Architecture/2026-11-19/core-logger-service.md) and [LLM activity logging](/docs/adr/Architecture/2026-11-19/llm-activity-logging.md) decisions require logs to come only from language-model calls. The [adapter-only boundary](/app/llm/docs/adr/11-14-26/adapter-only-boundary.md) decision prevents the LLM component from defining application-level records or performing application operations.

## Decision

- Add a logging adapter under `app/llm/adapters/` that implements the Core-owned `LLMPort`.
- The logging adapter wraps another `LLMPort`, measures duration and memory, delegates the call unchanged, and reports the outcome to the Core-owned LLM logger.
- Extend the Core LLM port result to carry response content, finish reason, and token usage while keeping the LLM Service's public return value unchanged.
- Read usage and finish reason from the provider response inside the Ollama adapter.
- Wire the logging adapter in `create_llm_service` only when a logger is supplied.
- Log structured generation calls only.

## Consequences

- Logging is provider-agnostic at the wrapper level while provider-specific response fields are parsed by the Ollama adapter.
- Existing LLM callers continue to receive a plain structured response object.
- Errors and results propagate unchanged when logging fails or succeeds.
- The LLM component still contains adapters only and defines no application records.
