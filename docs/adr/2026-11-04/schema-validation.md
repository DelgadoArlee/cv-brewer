# Use JSON Schema and Pydantic for data validation

## Date

2026-11-04

## Status

Accepted

## Context

Resume, job description, and generated resume data must conform to defined structures before storage or output. The project documentation defines JSON models and requires deterministic schema validation. Runtime models also need type safety.

## Decision

Use JSON Schema Draft 2020-12 as the contract for resume, job description, and generated resume data. Use Pydantic v2 for runtime models and serialization. Use the `jsonschema` library to validate data against the versioned schema files.

Store schemas in the repository and validate at system boundaries before storage, generation, or rendering.

## Consequences

- Schema violations produce deterministic, reportable errors.
- Pydantic provides typed models and reduces ad hoc validation code.
- JSON Schema and Pydantic models must be kept in sync; tests should verify they agree.
- Schema changes require coordinated updates to schemas, models, validation, and documentation.
