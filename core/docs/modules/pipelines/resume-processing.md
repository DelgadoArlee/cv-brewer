# Resume Processing Processor Module Technical Specification

## 1. Purpose

Coordinates the resume-processing pipeline for each supplied file and returns a final outcome without allowing one file failure to stop other files. The implementation is located at `core/src/core/pipeline/resume_processing.py`.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `ResumeProcessor` | Class | Coordinates validation, extraction, parsing, schema validation, deduplication, and storage. | `resume_service: ResumeService`, `llm_service: LLMService` – Service interfaces. | `ResumeProcessor` instance. |
| `StageCallback` | Type alias | Callback invoked with the current processing stage key while a resume is processed. | `stage: str` – Processing stage key. | `None`. |
| `ResumeProcessor.process()` | Method | Processes one supplied resume file and optionally reports the current processing stage through a callback. | `resume_input: ResumeInput` – File bytes and metadata; `on_stage: StageCallback | None` – Optional stage notification callback. | `ResumeProcessingOutcome` – Final outcome. |
| `ResumeProcessor.process_many()` | Method | Processes multiple supplied resume files independently and optionally reports the current processing stage through a callback. | `resume_inputs: Iterable[ResumeInput]` – Files to process; `on_stage: StageCallback | None` – Optional stage notification callback. | `list[ResumeProcessingOutcome]` – Outcomes in input order. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| Database Service `ResumeService` | Internal interface | Finds duplicates and stores validated resumes. |
| LLM Service `LLMService` | Internal interface | Resolves the parsing model and generates structured data. |
| Resume processing modules | Internal modules | Provide metadata, validation, extraction, parsing, and schema validation. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/12/2026 | Store successful resumes through the Database Service and return per-file outcomes. | `ResumeProcessor`, `ResumeProcessor.process()`, `ResumeProcessor.process_many()` | [Resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md) |

## 5. References

- [Resume Processing Technical System Specification](../../systems/resume-processing/overview.md)
- [Resume Processing Models Module](../models/models.md)
- [Resume Processing Process](../../../../docs/system/resume-processing/processes/resume-processing.md)
- [Store Resume Process](../../../../docs/system/database-service/processes/store-resume.md)
- [Establish the resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md)
