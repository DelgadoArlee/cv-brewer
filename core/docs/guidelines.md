# Core Component Guidelines

## Package Structure

1. Place pipeline processes in `core/src/core/pipeline/`.
2. Place non-validation modules in `core/src/core/modules/`.
3. Place validation modules in `core/src/core/validation/`.
4. Place validation Pydantic models in `core/src/core/validation/models/` and JSON Schemas in `core/src/core/validation/schemas/`.
5. Place non-validation models in `core/src/core/models/`.
6. Keep shared Core errors in `core/src/core/errors.py`.

## Rules

- Keep pipeline orchestration separate from reusable processing modules.
- Keep validation logic and validation models together under `validation/`.
- Use absolute imports.
- Do not add packages or move code between these layers without an approved decision.
