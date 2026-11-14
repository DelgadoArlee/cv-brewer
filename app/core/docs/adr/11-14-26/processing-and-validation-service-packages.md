# Organize Processing and Validation Code by Service Packages

## Date

2026-11-14

## Status

Accepted

## Context

Processing code is organized under `app/core/services/<service-name>/`, but validation code remained centralized under `app/core/validation/`. File signature validation belongs to PDF processing, while resume schema validation, validation models, and the Resume JSON Schema belong to the resume service that produces and validates resume records. Keeping validation outside those services obscures ownership and splits related code across package boundaries.

## Decision

- Place each processing module and its validation functions under its own service package as `app/core/services/<service-name>/service.py`.
- Place PDF signature verification in `app/core/services/pdf/service.py`.
- Place resume schema validation in `app/core/services/resume/service.py`.
- Place only validation Pydantic models in `app/core/services/resume/validation/models/`.
- Place only validation JSON Schemas in `app/core/services/resume/validation/schemas/`.
- Export public validation functions from each service package `__init__.py`.
- Do not create validation packages for validation functions.
- Remove the `app/core/validation/` package.
- Keep pipeline processes under `app/core/pipeline/`, non-validation models under `app/core/models/`, and shared errors in `app/core/errors.py`.

This supersedes the validation placement in [Organize processing modules as services](../11-13-26/processing-service-packages.md).

## Consequences

- Pipeline code imports PDF validation from `core.services.pdf` and resume validation from `core.services.resume`.
- Parsing imports the Resume JSON Schema loader from `core.services.resume`.
- Validation behavior is unchanged.
- Validation functions follow the same service package boundary as the processing code they support.
- Validation models and JSON Schemas remain under the owning service's `validation/` package.
