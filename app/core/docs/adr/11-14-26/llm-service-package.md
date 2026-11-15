# Establish the LLM Service Package

## Date

2026-11-14

## Status

Accepted

## Context

The LLM Service application layer is now owned by the Core under the [Move the LLM Service into the Core application layer](../../../../../docs/adr/Architecture/2026-11-14/llm-service-to-core.md) decision. All LLM request records, the adapter contract, and LLM service operations previously lived under the LLM component. Core needs a package location that keeps LLM-specific application logic together without reintroducing a generic LLM abstraction that has no shared use yet.

## Decision

- Place all LLM-specific service code under `app/core/services/llm/`.
- Define LLM request records in `app/core/services/llm/models.py`.
- Define the LLM adapter contract as `LLMPort` in `app/core/services/llm/port.py`.
- Define LLM service operations in `app/core/services/llm/service.py`.
- Export the LLM records, `LLMPort`, and `LLMService` from `app/core/services/llm/__init__.py`.
- Do not create a reusable LLM abstraction package until a concrete shared need exists.

## Consequences

- Core owns all LLM-specific application-level code.
- LLM adapters import the Core-owned LLM records and the `LLMPort` contract.
- The former `app/llm/llm_service/` package is removed.
- New LLM services follow the `services/llm/` package structure.
- Reusable LLM abstractions are deferred until a shared need exists.
