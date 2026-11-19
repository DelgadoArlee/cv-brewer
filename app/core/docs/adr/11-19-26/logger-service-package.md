# Establish the Logger Service Package

## Date

2026-11-19

## Status

Accepted

## Context

The [Core-owned Logger Service](/docs/adr/Architecture/2026-11-19/core-logger-service.md) decision requires a reusable logging engine with pluggable destinations. Core needs a package layout that keeps generic logging separate from LLM-specific log construction while following the existing `services/<name>/` convention.

## Decision

- Place generic logging under `app/core/services/logger/`.
- Define the generic log record and status values in `models.py`.
- Define performance measurement in `performance.py`.
- Define the sink contract in `port.py`.
- Define logging operations in `service.py` and export the public API from `__init__.py`.
- Define LLM-specific log records, repository contract, and logger under `app/core/services/llm/` without moving generic logging concerns into the LLM service.

## Consequences

- Generic logging can be reused without depending on LLM-specific record shapes.
- LLM logging is a specialization of the generic logger.
- Destination adapters implement Core-owned contracts rather than defining application records.
