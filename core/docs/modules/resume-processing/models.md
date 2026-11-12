# Resume Processing Models Module Technical Specification

## 1. Purpose

Defines the Core-facing input, status, outcome, and configuration records used by the resume-processing system. The implementation is located at `core/src/core/models/`.

## 2. Code Elements

| Element                   | Type      | Description                                            | Arguments / Parameters                                                                                      | Return Value / Result                                                                                                                     |
| ------------------------- | --------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `ResumeInput`             | Dataclass | Holds supplied file bytes and metadata for processing. | `file_name`, `original_file_path`, `content`, optional `upload_timestamp`.                                  | `ResumeInput` instance.                                                                                                                   |
| `ResumeProcessingStatus`  | Enum      | Identifies the final outcome of a processed file.      | None.                                                                                                       | Stored, duplicate, invalid file type, invalid PDF, unreadable, schema invalid, LLM failure, storage failure, or processing failure value. |
| `ResumeProcessingOutcome` | Dataclass | Reports the final result of processing one file.       | `file_name`, `status`, `message`, optional `resume_id`, optional `duplicate_resume_id`, processing history. | `ResumeProcessingOutcome` instance.                                                                                                       |

## 3. Dependencies

| Name                                        | Type                | Purpose                                 |
| ------------------------------------------- | ------------------- | --------------------------------------- |
| Python `dataclasses`                        | Standard library    | Defines immutable processing records.   |
| Python `enum`                               | Standard library    | Defines processing statuses.            |
| Database Service processing history records | Internal dependency | Reports processing history in outcomes. |

## 4. Architecture Decision Log

| Date       | Decision / Description                                           | Affected Code Elements                                             | Reference                                                                          |
| ---------- | ---------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| 11/12/2026 | Added Core resume-processing input, status, and outcome records. | `ResumeInput`, `ResumeProcessingStatus`, `ResumeProcessingOutcome` | [Resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md) |

## 5. References

- [Resume Processing Technical System Specification](../../systems/resume-processing/overview.md)
- [Resume Processing Processor Module](resume-processing.md)
- [Establish the resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md)
