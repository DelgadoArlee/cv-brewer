# Core Component Architecture Decision Log

This log indexes the component-level Architecture Decision Records (ADRs) for the Core component. Entries are ordered with the newest decisions first.

| Date | Decision | Status |
| --- | --- | --- |
| 2026-11-12 | [Report resume processing stages to callers](11-12-26/stage-progress-reporting.md) — Expose an optional stage notification callback from `ResumeProcessor.process()` and `process_many()`. | Accepted |
| 2026-11-12 | [Organize Core packages by responsibility](11-12-26/core-package-structure.md) — Separate pipeline processes, modules, validation, and models into dedicated packages and keep shared errors at the Core package root. | Accepted |
| 2026-11-12 | [Establish the resume-processing foundation](11-12-26/resume-processing-foundation.md) — Use raw-byte fingerprinting, first-available LLM model selection, always-on LLM enhancement, basic deterministic parsing, and a schema derived from the user resume data model. | Accepted |
