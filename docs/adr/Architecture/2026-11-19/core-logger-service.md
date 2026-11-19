# Add a Core-Owned Logger Service

## Date

2026-11-19

## Status

Accepted

## Category

architecture

## Context

CVBrewer has no logging service. Individual workflows record their own processing history, but there is no reusable way to record structured activity information and route it to one or more destinations. A new log-query CLI needs a stable source of structured log records, and future logging needs should not require rebuilding each logger from scratch.

## Decision

- Introduce a reusable Logger Service in the Core application layer.
- Define a generic log record and a sink contract in Core so log records can be written to one or more destinations.
- Keep logging destinations outside Core; Database implements the destination used for persisted logs.
- Build LLM-specific logging on top of the generic Logger Service.
- Record LLM activities only. Do not record general application events, PDF processing, database operations, or non-LLM performance metrics through this service.

## Consequences

- Core owns log record definitions and logging behavior; adapters own destination-specific writing.
- Additional destinations can be added by implementing the Core-owned sink contract.
- LLM-specific log records are application data owned by Core and persisted through the Database Adapter.
- Documentation and tests must cover the new service before use.
