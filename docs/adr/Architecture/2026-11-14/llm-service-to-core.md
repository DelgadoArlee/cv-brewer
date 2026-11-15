# Move the LLM Service into the Core Application Layer

## Date

2026-11-14

## Status

Accepted

## Category

architecture

## Context

The LLM Service previously lived in the LLM component alongside the LLM Adapter. The Core depended on the LLM Service for application-level language-processing operations, while the LLM component owned both the application-level service and service-specific adapters.

The application-level LLM operations, request records, and adapter contract are Core concerns. Keeping them in the LLM component blurred the boundary between application logic and service-specific implementation, in contrast to the Database Service, which is already owned by Core while its adapters remain in the Database component.

## Decision

- Move the LLM Service application layer into the Core component.
- Place all LLM-specific service code under `app/core/services/llm/`, including LLM request records, the adapter contract, and LLM service operations.
- Name the Core-owned adapter contract `LLMPort` in `app/core/services/llm/port.py`.
- Keep LLM Adapters in the LLM component under `app/llm/adapters/`.
- LLM Adapters implement the Core-owned `LLMPort` contract.
- Keep the `create_llm_service` composition helper in `app/llm/__init__.py`.
- Do not introduce a reusable LLM abstraction package until a concrete shared need exists.
- The Core must not import LLM adapters, `httpx`, or Ollama-specific modules directly.

## Consequences

- Core owns application-level language-model operations while the LLM component owns service-specific implementation.
- LLM adapters depend on the Core-owned LLM service contract.
- The LLM component is bounded around adapters rather than application-level operations.
- Import paths, tests, and component documentation must be updated.
- The existing Ollama adapter decision remains in effect; this decision changes service ownership and code placement, not the adapter technology or behavior.
