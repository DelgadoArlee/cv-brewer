# LLM Service System Overview

## 1. Purpose

The LLM Service provides the application-level operations used to perform language-processing tasks with an external LLM service. It defines what LLM operations are available while delegating service-specific communication to an LLM Adapter.

## 2. Objectives

- Provide stable language-model operations for the Core Processing Engine.
- Verify that the configured LLM service is available before processing.
- List the models available on the configured LLM service.
- Generate schema-constrained structured responses for processing workflows.
- Keep LLM service implementation details outside application-level operations.
- Delegate communication, response handling, and error translation to the selected LLM Adapter.

## 3. Scope

### In Scope

- Application-level LLM operations: availability checking, model discovery, and structured response generation.
- Generation request and model record definitions used by the service boundary.
- Coordination with an LLM Adapter implementation.
- Reporting adapter failures to callers.

### Out of Scope

- Ollama HTTP communication, endpoints, and service-specific error handling.
- Prompt construction and JSON Schema selection, which belong to the Core.
- Schema validation of generated content, which belongs to the Core's validation workflows.
- CLI user interaction and LLM selection presentation.

## 4. Workflow

The service receives application-level LLM requests, verifies the request is complete, delegates the operation to the configured LLM Adapter, and returns the availability outcome, the available models, or the generated structured response.

See the [Check LLM Availability Process](processes/check-llm-availability.md), the [List Available Models Process](processes/list-available-models.md), and the [Generate Structured Response Process](processes/generate-structured-response.md).

## 5. Constraints

- The service must not depend on Ollama, `httpx`, or a specific LLM implementation.
- All LLM communication must be performed through an LLM Adapter implementation.
- The service must not construct prompts or select JSON Schemas.
- The service must not validate generated content against application schemas.

## 6. Rules

- Generation requests must identify a model, provide at least one prompt message, and include a JSON Schema before processing.
- Incomplete generation requests must be rejected before the adapter is called.
- Model listings must return an empty listing when the configured service provides no models.
- Adapter failures must be reported to the caller.

## 7. Error Handling

- LLM adapter failures must be reported to the caller.
- Unreachable LLM services must be reported as unavailable outcomes.
- Incomplete generation requests must be rejected before communication is attempted.

## 8. References

- [LLM Component Technical Specification](../../../app/llm/docs/technical-specification.md)
- [LLM Service Technical Specification](../../../app/llm/docs/systems/llm-service/overview.md)
- [Use an LLM Service abstraction with pluggable LLM adapters](../../adr/Architecture/2026-11-11/llm-service-abstraction.md)
