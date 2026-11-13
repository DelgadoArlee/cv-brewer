# Establish the Ollama adapter foundation

## Date

11/11/2026

## Status

Accepted

## Context

The LLM Service requires a first adapter implementation that communicates with the user's locally served Ollama service. The adapter must own all Ollama-specific communication, configuration, and error handling while remaining behind the LLM Service boundary, as established by the [LLM Service abstraction decision](../../../../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md).

## Decision

- Use a synchronous `httpx.Client` for all Ollama communication.
- Define an `OllamaConfig` dataclass that holds the service base URL (default `http://localhost:11434`) and separate connect and read timeouts.
- Verify availability through a lightweight version request.
- List models from the service model listing endpoint.
- Generate structured responses through the chat endpoint with streaming disabled and the JSON Schema passed through Ollama's structured-output `format` field.
- Parse the response message content as a JSON object and report invalid content as a response failure.
- Translate transport, timeout, response, and missing-model failures into the adapter-local error hierarchy.

## Consequences

- All Ollama API details remain inside `app/llm/adapters/ollama/`.
- Structured output quality depends on the configured Ollama model and version.
- Long generations are bounded by the configured read timeout.
- The adapter can be replaced or extended for other services without touching the LLM Service.
