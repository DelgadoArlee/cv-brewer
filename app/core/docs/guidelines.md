# Core Component Guidelines

## Package Structure

1. Place pipeline processes in `app/core/pipeline/`.
2. Place non-validation modules in `app/core/modules/`.
3. Place validation modules in `app/core/validation/`.
4. Place validation Pydantic models in `app/core/validation/models/` and JSON Schemas in `app/core/validation/schemas/`.
5. Place non-validation models in `app/core/models/`.
6. Keep shared Core errors in `app/core/errors.py`.

## Rules

- Keep pipeline orchestration separate from reusable processing modules.
- Keep validation logic and validation models together under `validation/`.
- Use absolute imports.
- Do not add packages or move code between these layers without an approved decision.
