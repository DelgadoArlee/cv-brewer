# Organize Core Packages by Responsibility

## Date

2026-11-12

## Status

Superseded by [Organize processing modules as services](../11-13-26/processing-service-packages.md).

## Context

The Core resume-processing implementation was organized under a single `app/core/resume_processing/` package. As Core grows, mixing pipeline orchestration, processing modules, validation, and models in one package makes responsibilities and dependencies harder to see. Core needs a consistent package structure aligned with the architecture organization.

## Decision

- Organize pipeline processes under `app/core/pipeline/`.
- Organize non-validation modules under `app/core/modules/`.
- Organize validation modules and validation Pydantic models under `app/core/validation/`, with JSON Schemas under `app/core/validation/schemas/`.
- Organize non-validation models under `app/core/models/`.
- Keep shared Core errors in `app/core/errors.py`.
- Define package structure rules in `app/core/docs/guidelines.md`.

This supersedes the single-package organization in the [Resume-processing foundation](resume-processing-foundation.md).

## Consequences

- Imports and schema resource paths use the new package locations.
- Resume-processing behavior is unchanged.
- New Core processes and modules follow the responsibility-based package structure.
