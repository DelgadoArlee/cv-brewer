# Use pypdf and pdfplumber for PDF processing

## Date

2026-11-04

## Status

Accepted

## Context

The Core must verify PDF file signatures, detect encryption, validate structural integrity, extract text, and generate content fingerprints. The implementation must remain compatible with single-executable packaging and avoid unnecessary native dependencies. Scanned or image-only PDFs are rejected by the requirements.

## Decision

Use a direct `%PDF-` signature check for file-type verification. Use `pypdf` for encryption status, document structure, page metadata, and metadata extraction. Use `pdfplumber` and `pdfminer.six` for text extraction. Use SHA-256 through Python's standard library for content fingerprints.

Avoid `pikepdf` initially to keep packaging simple; add it later only if structural validation requires qpdf-level handling.

## Consequences

- PDF processing remains pure Python and easier to package across operating systems.
- Some malformed or unusual PDFs may require a more capable library such as `pikepdf` in the future.
- Text extraction quality depends on the source PDF; image-only PDFs remain unsupported.
- PDF libraries and their data files must be included in the packaged executable.
