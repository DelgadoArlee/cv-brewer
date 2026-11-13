# LLM Component Coding Guidelines

## LLM Service Code

- Service modules must be stored under `llm/src/llm/llm_service/modules/<module-name>/`.
- Each module must own one application-level LLM responsibility.
- Service modules define application-level operations and must not contain service-specific communication, HTTP clients, endpoints, or service-specific error handling.

## LLM Adapter Code

- Adapter implementations must be stored under `llm/src/llm/adapters/<adapter-name>/`.
- Adapters must own service communication, configuration, response parsing, and error translation.
- Adapter internals must remain service-specific and must not leak into the LLM Service or other components.
