# Report Resume Processing Stages to Callers

## Date

2026-11-12

## Status

Accepted

## Context

Resume processing can take a noticeable amount of time, especially during LLM enhancement. The CLI upload workflow shows a progress indicator, but it could only report file-level progress, not the processing stage currently running inside the Core Processing Engine.

## Decision

- `ResumeProcessor.process()` and `process_many()` accept an optional `on_stage` callback.
- The callback receives the current processing stage key as its only argument.
- Stage keys match the step names already recorded in `processing_history`: `file_type_validation`, `metadata_extraction`, `deduplication`, `pdf_validation`, `content_extraction`, `parsing`, `schema_validation`, and `storage`.
- The callback is invoked at the start of each stage and is optional, so existing callers continue to work unchanged.
- The CLI uses the callback to update its inline progress description during upload.

## Consequences

- The Core Processing Engine remains independent of Rich and other presentation concerns.
- Callers can provide live stage feedback without changing processing outcomes or history.
- Stage reporting adds a small, optional coupling between the Core and its callers through a callback contract.
