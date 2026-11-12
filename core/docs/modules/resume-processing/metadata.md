# Resume Processing Metadata Module Technical Specification

## 1. Purpose

Builds the file metadata required by the resume-processing pipeline and computes the raw-byte content fingerprint used for deduplication. The implementation is located at `core/src/core/modules/metadata.py`.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `calculate_content_fingerprint()` | Function | Computes the SHA-256 hex digest of supplied bytes. | `content: bytes` – Raw uploaded file bytes. | `str` – SHA-256 hex digest. |
| `resolve_upload_timestamp()` | Function | Returns the supplied timestamp or the current UTC timestamp without timezone metadata. | `upload_timestamp: datetime \| None` – Optional supplied timestamp. | `datetime` – Upload timestamp. |
| `build_resume_metadata()` | Function | Builds Database Service resume metadata. | `resume_input: ResumeInput` – File input record. | `ResumeMetadata` – File name, size, upload timestamp, and fingerprint. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| Python `hashlib` | Standard library | Computes SHA-256 fingerprints. |
| Python `datetime` | Standard library | Supplies and normalizes timestamps. |
| Database Service resume models | Internal dependency | Provides the `ResumeMetadata` record. |
| Resume processing models | Internal module | Provides `ResumeInput`. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/12/2026 | Use SHA-256 over raw file bytes for deduplication. | `calculate_content_fingerprint()`, `build_resume_metadata()` | [Resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md) |

## 5. References

- [Resume Processing Technical System Specification](../../systems/resume-processing/overview.md)
- [Resume Processing Models Module](../models/models.md)
- [Metadata Extraction Process](../../../../docs/system/resume-processing/processes/2-metadata-extraction.md)
- [Establish the resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md)
