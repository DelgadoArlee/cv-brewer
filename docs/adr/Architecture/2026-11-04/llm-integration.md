# Integrate local LLMs through a native Ollama adapter

## Date

2026-11-04

## Status

Superseded by [Use an LLM Service abstraction with pluggable LLM adapters](../2026-11-11/llm-service-abstraction.md)

## Context

Normal operation must use a locally served LLM that the user installs and configures. The LLM is external and is not bundled. The LLM Provider and LLM Adapter must isolate model-specific communication from the Core. Ollama is available on Windows, macOS, and Linux.

## Decision

Use a native Ollama adapter through `httpx` as the first LLM integration. The adapter communicates with the user's Ollama service, checks availability, sends structured prompts, and requests JSON-formatted responses.

The LLM Provider manages prompt construction, context preparation, and error reporting. The application does not bundle a model or require a cloud service. Additional adapters, including OpenAI-compatible services, may be added later.

## Consequences

- Users must install and run Ollama for normal operation.
- Ollama API or model behavior changes may require adapter updates.
- Structured output support depends on the configured Ollama model and version.
- The Provider/Adapter boundary keeps the Core independent of Ollama-specific details.
