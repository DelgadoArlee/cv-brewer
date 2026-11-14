# Organize Processing Modules as Services

## Date

2026-11-13

## Status

Superseded by [Organize processing and validation code by service packages](../11-14-26/processing-and-validation-service-packages.md).

## Context

Core processing code was split between `app/core/services/resume/` and `app/core/modules/`. Metadata extraction, PDF processing, and parsing lived as standalone modules while resume data operations already used a service package. This made processing responsibilities inconsistent and obscured the service boundary used by pipeline orchestration.

## Decision

- Place each non-validation processing module under its own service package as `app/core/services/<service-name>/service.py`.
- Place metadata extraction in `app/core/services/metadata/service.py`.
- Place PDF processing in `app/core/services/pdf/service.py`.
- Place parsing in `app/core/services/parsing/service.py`.
- Export public service functions from each service package `__init__.py`.
- Remove the `app/core/modules/` package.
- Keep pipeline processes under `app/core/pipeline/`, validation under `app/core/validation/`, non-validation models under `app/core/models/`, and shared errors in `app/core/errors.py`.

This supersedes the `app/core/modules/` placement in [Organize Core packages by responsibility](../11-12-26/core-package-structure.md).

## Consequences

- Pipeline and tests import processing functions from `core.services.<service-name>`.
- Resume-processing behavior is unchanged.
- Future non-validation processing modules follow the `services/<service-name>/service.py` structure.
- Core processing responsibilities are consistently organized under service packages.
