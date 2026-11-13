# LLM Component Technical Specification

## 1. Purpose

This document defines the technical organization of the LLM component within CVBrewer. It describes how the LLM Service and LLM Adapter are structured and bounded so language-processing tasks can be performed without coupling the rest of the application to a specific LLM service.

## 2. Objective

- Provide a stable application-level language-model boundary for the Core Processing Engine.
- Keep LLM-service-specific concerns inside adapter implementations.
- Support Ollama as the default LLM service implementation through `httpx`.
- Allow future LLM services to be added through compatible adapters without changing application-level LLM operations.
- Keep the LLM component within the single Python distribution used by the application.

## 3. Scope

### In Scope

- The LLM component package and its internal subpackages.
- LLM Service application-level operations and boundaries.
- LLM Adapter implementation boundaries.
- LLM service communication, configuration, response parsing, and error translation within adapters.
- Component technical documentation.

### Out of Scope

- Core Processing Engine resume processing and generation workflows.
- CLI user interaction and file-system management.
- Prompt construction and JSON Schema selection, which belong to the Core.
- Schema validation of generated content against application schemas.
- Model installation, downloading, and management.
- Implementation code and test cases.

## 4. Rules & Constraints

- The LLM Service must define the application-level operations required by the application: availability checking, model discovery, and structured response generation.
- The LLM Service must not contain service-specific communication, HTTP clients, service endpoints, or service-specific error handling.
- All LLM communication must be performed through the selected LLM Adapter.
- The LLM Adapter must own service communication, configuration, response parsing, and service-specific error translation.
- The Core Processing Engine must depend only on the LLM Service operations and must not import `httpx` or Ollama-specific modules directly.
- Ollama is the default LLM service implementation, accessed through `httpx`.
- LLM-service-specific implementation details must remain isolated to adapter packages.
- Structured responses must be returned as JSON objects; validation against application schemas is performed by the Core.
- The application must not bundle a model or require a cloud service for normal operation.
- LLM Service and LLM Adapter code organization must follow the [LLM Component Coding Guidelines](guidelines.md).
- The LLM component must remain part of the single Python distribution and must not be independently deployed.

## 5. Architectural & Design Approaches

### 5.1. Service–Adapter Separation

- **Name:** Service–Adapter separation.
- **Description:** Application-level LLM operations are separated from service-specific implementation details.
- **Application:** The LLM Service defines the operations required by the application, and the LLM Adapter carries out those operations using the selected LLM service.

### 5.2. Adapter Pattern

- **Name:** Adapter pattern.
- **Description:** A stable component interface is implemented by LLM-service-specific adapters.
- **Application:** The Ollama adapter uses `httpx`, and future LLM services can be supported by providing compatible adapters without changing the LLM Service.

### 5.3. Single-Project Internal Packaging

- **Name:** Single-project internal packaging.
- **Description:** The LLM component is maintained as one Python project containing internal packages.
- **Application:** The LLM Service and LLM adapter implementations are organized under `llm/src/llm/` as separate internal packages.

## 6. Systems

| System     | Description                                                                                          | Specification                                              |
| ---------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| LLM Service | Manages application-level LLM operations and coordinates requests through the selected LLM Adapter. | [LLM Service](systems/llm-service/overview.md)            |
| LLM Adapter | Implements LLM-service-specific communication, configuration, response parsing, and error translation. | [LLM Adapter](systems/llm-adapter/overview.md)            |

## 7. File Structure

````text
llm/
├── pyproject.toml          Project configuration and package metadata.
├── README.md               Package README file.
├── .python-version         Python version selection.
├── docs/
│   ├── technical-specification.md
│   ├── guidelines.md
│   ├── adr/
│   │   ├── ADL.md
│   │   └── 11-11-26/
│   │       └── ollama-adapter-foundation.md
│   └── systems/
│       ├── llm-service/
│       │   ├── overview.md
│       │   └── processes/
│       │       ├── check-llm-availability.md
│       │       ├── generate-structured-response.md
│       │       └── list-available-models.md
│       └── llm-adapter/
│           ├── overview.md
│           └── processes/
│               ├── generate-structured-response.md
│               ├── list-service-models.md
│               └── verify-service-availability.md
└── src/
    └── llm/
        ├── __init__.py
        ├── llm_service/
        │   ├── __init__.py
        │   └── modules/
        │       └── generation/
        │           ├── __init__.py
        │           ├── models.py
        │           ├── adapter.py
        │           └── service.py
        └── adapters/
            ├── __init__.py
            └── ollama/
                ├── __init__.py
                ├── adapter.py
                ├── config.py
                └── errors.py
````

## 8. Deployment

- The LLM component is included in the single CLI/Core executable.
- The external LLM service, such as the user's Ollama installation, is installed, configured, and operated separately from the application.
- Model files are deployed with the external LLM service and are never bundled with the application.
- The LLM service endpoint and timeouts are configured through the selected adapter; the default endpoint is the local Ollama service.

## 9. References

- [System Architecture](../../docs/architecture.md)
- [Repository Architecture](../../docs/repository/architecture.md)
- [Tech Stack](../../docs/tech-stack.md)
- [Requirements](../../docs/requirements.md)
- [General System Rules](../../docs/system-rules.md)
- [LLM Service System Overview](../../docs/system/llm-service/overview.md)
- [LLM Adapter System Overview](../../docs/system/llm-adapter/overview.md)
- [Use an LLM Service abstraction with pluggable LLM adapters](../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md)
- [Integrate local LLMs through a native Ollama adapter](../../docs/adr/Architecture/2026-11-04/llm-integration.md) — superseded by the LLM Service abstraction
- [LLM Component Coding Guidelines](guidelines.md)
- [LLM Service System Specification](systems/llm-service/overview.md)
- [LLM Adapter System Specification](systems/llm-adapter/overview.md)
