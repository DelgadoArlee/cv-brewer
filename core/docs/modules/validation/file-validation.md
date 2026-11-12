# Resume Processing File Validation Module Technical Specification

## 1. Purpose

Verifies that supplied bytes begin with the PDF file signature before any other processing occurs. The implementation is located at `core/src/core/validation/file_validation.py`.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `verify_pdf_signature()` | Function | Checks the PDF signature and raises a validation error when it is absent. | `content: bytes` – Raw uploaded file bytes. | `None`; raises `InvalidFileTypeError` when invalid. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| Resume processing errors | Internal module | Provides `InvalidFileTypeError`. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/12/2026 | Verify the `%PDF-` signature on raw bytes. | `verify_pdf_signature()` | [Resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md) |

## 5. References

- [Resume Processing Technical System Specification](../../systems/resume-processing/overview.md)
- [File Type Verification Process](../../../../docs/system/resume-processing/processes/1-file-type-verification.md)
- [Use pypdf and pdfplumber for PDF processing](../../../../docs/adr/Architecture/2026-11-04/pdf-processing.md)
