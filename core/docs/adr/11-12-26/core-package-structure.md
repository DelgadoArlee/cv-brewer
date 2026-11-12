# Organize Core Packages by Responsibility

## Date

2026-11-12

## Status

Accepted

## Context

The Core resume-processing implementation was organized under a single `core/src/core/resume_processing/` package. As Core grows, mixing pipeline orchestration, processing modules, validation, and models in one package makes responsibilities and dependencies harder to see. Core needs a consistent package structure aligned with the architecture organization.

## Decision

- Organize pipeline processes under `core/src/core/pipeline/`.
- Organize non-validation modules under `core/src/core/modules/`.
- Organize validation modules and validation Pydantic models under `core/src/core/validation/`, with JSON Schemas under `core/src/core/validation/schemas/`.
- Organize non-validation models under `core/src/core/models/`.
- Keep shared Core errors in `core/src/core/errors.py`.
- Define package structure rules in `core/docs/guidelines.md`.

This supersedes the single-package organization in the [Resume-processing foundation](resume-processing-foundation.md).

## Consequences

- Imports and schema resource paths use the new package locations.
- Resume-processing behavior is unchanged.
- New Core processes and modules follow the responsibility-based package structure.
