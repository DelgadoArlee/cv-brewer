# LLM Component Architecture Decision Log

This log indexes the Architecture Decision Records (ADRs) for the LLM component. Entries are ordered with the newest decisions first.

| Date       | Decision                                                       | Status  | High-Level ADR |
| ---------- | -------------------------------------------------------------- | ------- | -------------- |
| 11/19/2026 | [Capture LLM logs at the adapter boundary](/app/llm/docs/adr/11-19-26/logging-adapter.md) — Wrap the LLM port with logging, carry usage and finish reason on the port result, and wire logging through `create_llm_service`. | Accepted | [LLM Activity Logging](/docs/adr/Architecture/2026-11-19/llm-activity-logging.md) |
| 11/14/2026 | [Retain LLM Adapters as the LLM component boundary](/app/llm/docs/adr/11-14-26/adapter-only-boundary.md) — Keep adapters in the LLM component and implement the Core-owned `LLMPort` contract. | Accepted | [LLM Service in Core](/docs/adr/Architecture/2026-11-14/llm-service-to-core.md) |
| 11/11/2026 | [Establish the Ollama adapter foundation](/app/llm/docs/adr/11-11-26/ollama-adapter-foundation.md) — Use synchronous `httpx`, adapter-local configuration and errors, structured outputs through the chat endpoint. | Accepted | [LLM Service Abstraction](/docs/adr/Architecture/2026-11-11/llm-service-abstraction.md) |
