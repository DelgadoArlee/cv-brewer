# Use an LLM Service abstraction with pluggable LLM adapters

## Date

2026-11-11

## Status

Accepted

## Context

Normal operation must use a locally served LLM that the user installs and configures. The LLM is external and is not bundled. The Core must stay independent of any specific LLM service.

The 2026-11-04 LLM integration decision described a separate LLM Provider layer responsible for prompt construction, context preparation, and error reporting, placed between the Core and the LLM Adapter. A dedicated Provider layer duplicates the pluggability already provided by a service abstraction, and the Core already owns the task knowledge that prompts describe. Prompt construction therefore belongs with the Core's processing workflows.

## Decision

Replace the LLM Provider layer with an LLM Service abstraction modeled on the Database Service.

- The LLM Service defines application-level operations: verifying service availability, listing available models, and generating structured responses.
- The LLM Service delegates all service-specific communication to a configured LLM Adapter.
- LLM adapters implement the LLM Service operations for their service; the native Ollama adapter through `httpx` is the first implementation.
- The Core depends only on the LLM Service operations, constructs its own prompts, and supplies prompts together with JSON Schemas for structured generation requests.
- The Ollama adapter checks availability, lists models, and requests schema-constrained JSON-formatted responses.

## Consequences

- The Core must construct prompts and provide JSON Schemas for structured generation requests.
- Additional adapters, including OpenAI-compatible services, can be added without changing the Core or the LLM Service.
- Users must still install and run Ollama for normal operation.
- Ollama API or model behavior changes may require adapter updates.
- Structured output support depends on the configured Ollama model and version.
- This decision supersedes the Provider/Adapter split described in [Integrate local LLMs through a native Ollama adapter](../2026-11-04/llm-integration.md).
