# Resume Processing PDF Processing Module Technical Specification

## 1. Purpose

Validates PDF encryption and structure and extracts readable text from valid PDF documents. The implementation is located at `core/src/core/modules/pdf_processing.py`.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `validate_pdf()` | Function | Rejects encrypted, password-protected, structurally invalid, or page-less PDFs. | `content: bytes` – PDF file bytes. | `None`; raises `InvalidPdfError` when invalid. |
| `extract_pdf_text()` | Function | Extracts and joins text from all PDF pages and rejects documents without readable text. | `content: bytes` – PDF file bytes. | `str` – Extracted readable text. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `pypdf` | External library | Validates PDF encryption and document structure. |
| `pdfplumber` | External library | Extracts text from PDF pages. |
| Python `io` | Standard library | Supplies in-memory byte streams to PDF libraries. |
| Resume processing errors | Internal module | Provides `InvalidPdfError` and `UnreadableContentError`. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/12/2026 | Use `pypdf` for validation and `pdfplumber` for text extraction. | `validate_pdf()`, `extract_pdf_text()` | [Use pypdf and pdfplumber for PDF processing](../../../../docs/adr/Architecture/2026-11-04/pdf-processing.md) |

## 5. References

- [Resume Processing Technical System Specification](../../systems/resume-processing/overview.md)
- [PDF Validation Process](../../../../docs/system/resume-processing/processes/4-pdf-validation.md)
- [PDF Extraction Process](../../../../docs/system/resume-processing/processes/5-pdf-extraction.md)
- [Use pypdf and pdfplumber for PDF processing](../../../../docs/adr/Architecture/2026-11-04/pdf-processing.md)
