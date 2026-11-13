# Establish the Resume Processing Foundation

## Date

2026-11-12

## Status

Accepted

## Context

The Core Processing Engine has no resume-processing implementation. The high-level resume-processing documentation defines a pipeline for file-type validation, metadata extraction, deduplication, PDF validation, content extraction, parsing, schema validation, and storage, but it does not define several implementation decisions required to build the Core.

The Core must remain independent of the file system, SQLAlchemy, SQLite, and any specific LLM service. It receives file bytes from the CLI, uses the Database Service for persistence, and uses the LLM Service for structured generation.

## Decision

- Compute the deduplication content fingerprint as the SHA-256 hash of the raw uploaded file bytes.
- Select the first model returned by `LLMService.list_models()` for resume parsing enhancement.
- Always invoke LLM enhancement after deterministic extraction and merge the results.
- Use basic deterministic heuristics for contact information and common resume sections, then use the LLM to fill gaps and normalize the data.
- Derive the Resume JSON Schema from the `parsed_data` structure in the user resume data model.
- Accept a PDF when extracted text contains at least one non-whitespace character.
- Store successful resume records only through the Database Service.
- Organize the implementation as modules under `app/core/resume_processing/`.

## Consequences

- Deduplication is available before PDF validation and content extraction.
- Resume processing requires at least one model to be available through the configured LLM Service.
- Deterministic parsing remains intentionally limited; LLM availability is required for every processed file.
- The Resume JSON Schema and Pydantic models must remain aligned with the user resume data model.
- No resume record is stored for files that fail validation, parsing, schema validation, or storage.
