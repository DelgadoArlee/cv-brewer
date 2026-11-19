# LLM Component Technical Specification

## 1. Purpose

This document defines the technical organization of the LLM component within CVBrewer. It describes how LLM Adapters are structured and bounded so service-specific language-model operations can be implemented without coupling the Core application layer to a specific LLM service. Application-level language-model operations are owned by the Core.

## 2. Objective

- Provide adapter implementations for the Core-owned LLM port contract.
- Keep LLM-service-specific concerns inside adapter implementations.
- Support Ollama as the default LLM service implementation through `httpx`.
- Allow future LLM services to be added through compatible adapters without changing application-level LLM operations.
- Keep the LLM component within the single Python distribution used by the application.

## 3. Scope

### In Scope

- The LLM component package and its internal subpackages.
- LLM Adapter implementation boundaries.
- LLM service communication, configuration, response parsing, and error translation within adapters.
- Component technical documentation.

### Out of Scope

- Application-level LLM operations, request record definitions, and the adapter contract, which belong to the Core.
- Core Processing Engine resume processing and generation workflows.
- CLI user interaction and file-system management.
- Prompt construction and JSON Schema selection, which belong to the Core.
- Schema validation of generated content against application schemas.
- Model installation, downloading, and management.
- Implementation code and test cases.

## 4. Rules & Constraints

- The LLM Adapter must implement the port contract defined by the Core.
- The LLM component must not define application-level operations or application-level record structures.
- All LLM communication must be performed through the selected LLM Adapter.
- The LLM Adapter must own service communication, configuration, response parsing, and service-specific error translation.
- The Core Processing Engine must not import `httpx`, Ollama-specific modules, or LLM adapters directly.
- Ollama is the default LLM service implementation, accessed through `httpx`.
- LLM-service-specific implementation details must remain isolated to adapter packages.
- Structured responses must be returned as JSON objects; validation against application schemas is performed by the Core.
- The application must not bundle a model or require a cloud service for normal operation.
- LLM Adapter code organization must follow the [LLM Component Coding Guidelines](/app/llm/docs/guidelines.md).
- A logging adapter may wrap an LLM Adapter to observe generation calls, must implement the Core-owned `LLMPort`, and must not define application-level records.
- The LLM component must remain part of the single Python distribution and must not be independently deployed.

## 5. Architectural & Design Approaches

### 5.1. Adapter Layer for Core-Owned Service Contracts

- **Name:** Adapter layer for Core-owned service contracts.
- **Description:** Application-level LLM operations are separated from service-specific implementation details.
- **Application:** The Core defines the LLM port contract and service operations, and the LLM Adapter carries out those operations using the selected LLM service.

### 5.2. Adapter Pattern

- **Name:** Adapter pattern.
- **Description:** A stable Core-owned interface is implemented by LLM-service-specific adapters.
- **Application:** The Ollama adapter uses `httpx`, and future LLM services can be supported by providing compatible adapters without changing the Core service.

### 5.3. Single-Project Internal Packaging

- **Name:** Single-project internal packaging.
- **Description:** The LLM component is maintained as a module within the single application Python project.
- **Application:** LLM adapter implementations are organized under `app/llm/` and packaged with the other components by the `app/` project.

## 6. Systems

| System     | Description                                                                                          | Specification                                              |
| ---------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| LLM Adapter | Implements the Core-owned LLM port contract, service-specific communication, configuration, response parsing, and error translation. | [LLM Adapter](/app/llm/docs/system/llm-adapter/overview.md)            |

## 7. File Structure

````text
app/llm/
├── README.md               Component README file.
├── docs/
│   ├── technical-specification.md
│   ├── guidelines.md
│   ├── adr/
│   │   ├── ADL.md
│   │   ├── 11-11-26/
│   │   │   └── ollama-adapter-foundation.md
│   │   ├── 11-14-26/
│   │   │   └── adapter-only-boundary.md
│   │   └── 11-19-26/
│   │       └── logging-adapter.md
│   └── system/
│       └── llm-adapter/
│           ├── overview.md
│           └── processes/
│               ├── generate-structured-response.md
│               ├── list-service-models.md
│               ├── log-generation-call.md
│               └── verify-service-availability.md
├── __init__.py
└── adapters/
    ├── __init__.py
    ├── logging/
    │   ├── __init__.py
    │   └── adapter.py
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

- [System Architecture](/docs/architecture.md)
- [Repository Architecture](/app/README.md)
- [Tech Stack](/docs/tech-stack.md)
- [Requirements](/docs/requirements.md)
- [General System Rules](/docs/system-rules.md)
- [Core Component Technical Specification](/app/core/docs/technical-specification.md)
- [LLM Adapter System Overview](/docs/system/llm-adapter/overview.md)
- [LLM Component Coding Guidelines](/app/llm/docs/guidelines.md)
- [LLM Adapter System Specification](/app/llm/docs/system/llm-adapter/overview.md)
- [Move the LLM Service into Core](/docs/adr/Architecture/2026-11-14/llm-service-to-core.md)
- [Retain LLM Adapters as the LLM Component Boundary](/app/llm/docs/adr/11-14-26/adapter-only-boundary.md)
- [Capture LLM Logs at the Adapter Boundary](/app/llm/docs/adr/11-19-26/logging-adapter.md)
- [Log Generation Call Technical Process](/app/llm/docs/system/llm-adapter/processes/log-generation-call.md)
- [Use an LLM Service abstraction with pluggable LLM adapters](/docs/adr/Architecture/2026-11-11/llm-service-abstraction.md)
- [Integrate local LLMs through a native Ollama adapter](/docs/adr/Architecture/2026-11-04/llm-integration.md) — superseded by the LLM Service abstraction
