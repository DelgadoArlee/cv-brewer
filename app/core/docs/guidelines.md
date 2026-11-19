# Core Component Guidelines

## Package Structure

1. Place pipeline processes in `app/core/pipeline/`.
2. Place each processing module in its own service package under `app/core/services/<service-name>/service.py`.
3. Place resume-specific service code in `app/core/services/resume/`.
4. Place validation functions in the owning service's `app/core/services/<service-name>/service.py`.
5. Place only validation Pydantic models in `app/core/services/<service-name>/validation/models/` and JSON Schemas in `app/core/services/<service-name>/validation/schemas/`.
6. Place non-validation models in `app/core/models/`.
7. Keep shared Core errors in `app/core/errors.py`.
8. Place generic logging code in `app/core/services/logger/` and LLM-specific log records, logger, and repository contract in `app/core/services/llm/`.

## Rules

- Keep pipeline orchestration separate from reusable processing services.
- Keep each processing module under its own service package with a `service.py` module.
- Export public service functions from the service package `__init__.py`.
- Do not place processing code in an `app/core/modules/` package.
- Keep all resume-specific records, repository contracts, and service operations under `services/resume/`.
- Keep all LLM-specific records, the LLM port contract, and service operations under `services/llm/`.
- Keep all LLM-specific records, the LLM port contract, service operations, and LLM logging under `services/llm/`.
- Do not create reusable database or LLM abstractions until a concrete shared need exists; the generic Logger Service is an approved exception.
- Place validation functions in the owning service's `service.py`; do not create separate validation modules for functions.
- Place only validation Pydantic models and JSON Schemas under the owning service's `validation/` package.
- Import validation functions from the owning service package public API, not from validation subpackages.
- Do not create an `app/core/validation/` package or place validation models under `app/core/models/`.
- Use absolute imports.
- Service code must not import SQLAlchemy, SQLite, or database adapters.
- Service code must not import LLM adapters, `httpx`, or Ollama-specific modules.
- Do not add packages or move code between these layers without an approved decision.
