# LLM Component Architecture Decision Log

This log indexes the Architecture Decision Records (ADRs) for the LLM component. Entries are ordered with the newest decisions first.

| Date       | Decision                                                       | Status  |
| ---------- | -------------------------------------------------------------- | ------- |
| 11/14/2026 | [Retain LLM Adapters as the LLM component boundary](11-14-26/adapter-only-boundary.md) — Keep adapters in the LLM component and implement the Core-owned `LLMPort` contract. | Accepted |
| 11/11/2026 | [Establish the Ollama adapter foundation](11-11-26/ollama-adapter-foundation.md) — Use synchronous `httpx`, adapter-local configuration and errors, structured outputs through the chat endpoint. | Accepted |
