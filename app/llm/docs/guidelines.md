# LLM Component Coding Guidelines

## LLM Adapter Code

- Adapter implementations must be stored under `app/llm/adapters/<adapter-name>/`.
- Adapters must implement the Core-owned `LLMPort` contract.
- Adapters must own service communication, configuration, response parsing, and error translation.
- Adapter internals must remain service-specific and must not leak into the Core services or other components.
- Adapters must not define application-level operations or application-level record structures.
