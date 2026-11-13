# LLM Adapter System Overview

## 1. Purpose

The LLM Adapter implements LLM-service-specific operations for the LLM Service. It owns HTTP communication, request and response handling, and service-specific error translation so that application-level operations remain independent of a specific LLM service.

## 2. Objectives

- Verify the availability of the configured external LLM service.
- List the models available on the configured external LLM service.
- Generate schema-constrained structured responses from the selected model.
- Translate communication and response failures into adapter-level errors.

## 3. Scope

### In Scope

- Ollama HTTP communication through `httpx`: availability verification, model listing, and structured generation.
- Ollama service configuration, such as service URL and request timeouts.
- Response parsing and adapter error translation.

### Out of Scope

- Application-level LLM operation definitions, which belong to the LLM Service.
- Prompt construction and JSON Schema selection.
- Schema validation of generated content.
- CLI workflows and LLM selection presentation.

## 4. Workflow

The adapter receives operations from the LLM Service, communicates with the external LLM service, parses responses, and returns the availability outcome, the available models, the generated structured response, or a translated adapter error.

See the [Verify Service Availability Process](processes/verify-service-availability.md), the [List Service Models Process](processes/list-service-models.md), and the [Generate Structured Response Process](processes/generate-structured-response.md).

## 5. Constraints

- All LLM-service-specific implementation details must remain inside the adapter.
- Application-level LLM operation rules must remain in the LLM Service.
- The adapter must not construct prompts or validate content against application schemas.

## 6. Rules

- Communication failures must be translated to adapter-level connection errors.
- Request timeouts must be translated to adapter-level timeout errors.
- Failed or invalid responses must be translated to adapter-level response errors.
- Unavailable models must be translated to adapter-level model errors.
- Structured responses must be returned as JSON objects.

## 7. Error Handling

- Connection, timeout, response, and model failures must be translated and reported.
- Invalid structured response content must be reported as a response failure.

## 8. References

- [LLM Component Technical Specification](../../../app/llm/docs/technical-specification.md)
- [LLM Adapter Technical Specification](../../../app/llm/docs/systems/llm-adapter/overview.md)
- [Ollama Adapter Foundation ADR](../../../app/llm/docs/adr/11-11-26/ollama-adapter-foundation.md)
- [Use an LLM Service abstraction with pluggable LLM adapters](../../adr/Architecture/2026-11-11/llm-service-abstraction.md)
