# Core Component Architecture Decision Log

This log indexes the component-level Architecture Decision Records (ADRs) for the Core component. Entries are ordered with the newest decisions first.

| Date | Decision | Status | High-Level ADR |
| --- | --- | --- | --- |
| 2026-11-19 | [Establish the logger service package](/app/core/docs/adr/11-19-26/logger-service-package.md) — Place generic logging under `app/core/services/logger/` and LLM-specific log records, repository, and logger under `app/core/services/llm/`. | Accepted | [Core-owned Logger Service](/docs/adr/Architecture/2026-11-19/core-logger-service.md) |
| 2026-11-14 | [Establish the LLM service package](/app/core/docs/adr/11-14-26/llm-service-package.md) — Place all LLM-specific records, the `LLMPort` contract, and service operations under `app/core/services/llm/`. | Accepted | [LLM Service in Core](/docs/adr/Architecture/2026-11-14/llm-service-to-core.md) |
| 2026-11-14 | [Organize processing and validation code by service packages](/app/core/docs/adr/11-14-26/processing-and-validation-service-packages.md) — Place processing and validation functions under the owning service package, with only validation models and schemas under `validation/`. | Accepted | — |
| 2026-11-13 | [Organize processing modules as services](/app/core/docs/adr/11-13-26/processing-service-packages.md) — Place each non-validation processing module under its own service package. | Superseded | — |
| 2026-11-13 | [Establish the resume service package](/app/core/docs/adr/11-13-26/resume-service-package.md) — Place all resume-specific records, repository contracts, and service operations under `app/core/services/resume/`. | Accepted | — |
| 2026-11-12 | [Report resume processing stages to callers](/app/core/docs/adr/11-12-26/stage-progress-reporting.md) — Expose an optional stage notification callback from `ResumeProcessor.process()` and `process_many()`. | Accepted | — |
| 2026-11-12 | [Organize Core packages by responsibility](/app/core/docs/adr/11-12-26/core-package-structure.md) — Separate pipeline processes, modules, validation, and models into dedicated packages and keep shared errors at the Core package root. | Superseded | — |
| 2026-11-12 | [Establish the resume-processing foundation](/app/core/docs/adr/11-12-26/resume-processing-foundation.md) — Use raw-byte fingerprinting, first-available LLM model selection, always-on LLM enhancement, basic deterministic parsing, and a schema derived from the user resume data model. | Accepted | — |
