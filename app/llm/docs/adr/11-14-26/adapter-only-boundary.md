# Retain LLM Adapters as the LLM Component Boundary

## Date

2026-11-14

## Status

Accepted

## Context

The LLM Service application layer moved into the Core under `app/core/services/llm/` as part of the [Move the LLM Service into the Core application layer](../../../../../docs/adr/Architecture/2026-11-14/llm-service-to-core.md) decision. The LLM component must now define its boundary around service-specific adapters rather than application-level language-model operations. Structured generation still requires service-specific communication, configuration, response parsing, and error translation through the Ollama adapter.

## Decision

- Keep LLM Adapters under `app/llm/adapters/`.
- Implement the Core-owned `LLMPort` contract in `adapters/ollama/adapter.py`.
- Keep Ollama configuration and the adapter-local error hierarchy under `adapters/ollama/`.
- Preserve synchronous `httpx` communication, availability verification, model listing, and structured generation through the chat endpoint.
- Keep service communication, response parsing, and error translation inside the adapter.
- Do not define application-level operations or application-level record structures in the LLM component.
- Keep the `create_llm_service` composition helper in `app/llm/__init__.py`.

## Consequences

- The LLM component depends on Core-owned LLM service records and the `LLMPort` contract.
- Application-level LLM behavior changes belong in Core, not in the LLM component.
- The former `app/llm/llm_service/` package is removed.
- Future LLM adapters must provide compatible implementations of the Core-owned `LLMPort` contract.
- This decision supersedes the service-placement portions of [Use an LLM Service abstraction with pluggable LLM adapters](../../../../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md).
