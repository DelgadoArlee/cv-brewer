# PDF Extraction Technical Process

## 1. Purpose

Define how the Core Processing Engine extracts readable text from a validated PDF.

## 2. Objective

- Extract text from every PDF page.
- Produce a single text value for parsing.
- Reject documents without readable text.

## 3. Scope

### In Scope

- Page-by-page text extraction with `pdfplumber`.
- Joining page text into a single value.
- Rejecting documents with no non-whitespace text.

### Out of Scope

- PDF structure and encryption validation.
- OCR for image-only documents.
- Deterministic parsing and LLM enhancement.

## 4. Rules & Constraints

- Operate on validated PDF bytes only.
- Extract text from every page in page order.
- Treat missing page text as an empty string.
- Join page text with newline characters and trim surrounding whitespace.
- Reject the document when the extracted text is empty.
- Report extraction failures as unreadable content errors.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    Start([Validated PDF bytes]) --> Extract[Extract text from each page]
    Extract -->|Failure| Unreadable[Raise unreadable content error]
    Extract --> Join[Join page text and trim]
    Join --> Empty{Text empty?}
    Empty -->|Yes| Unreadable
    Empty -->|No| Return[Return extracted text]
````

### Steps

1. Open the validated PDF from the supplied bytes.
2. Extract text from each page in order.
3. Join the page text with newline characters and trim whitespace.
4. Raise an unreadable content error when extraction fails.
5. Raise an unreadable content error when the result is empty.
6. Return the extracted text for parsing.

## 6. Modules

- `core/src/core/modules/pdf_processing.py` — Implements PDF text extraction and readability checks.
- `core/src/core/pipeline/resume_processing.py` — Invokes extraction after PDF validation.
- `core/src/core/errors.py` — Defines the unreadable content error.

## 7. Testing

### 7.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| RP-EXT-001 | A PDF with readable text. | Text is extracted. | The combined text is returned. |
| RP-EXT-002 | A PDF with no readable text. | Text is extracted. | An unreadable content error is raised. |
| RP-EXT-003 | A PDF whose text extraction fails. | Text is extracted. | An unreadable content error is raised. |

## 8. References

- [Resume Processing Technical Process](resume-processing.md)
- [Resume Processing System Overview](../overview.md)
- [Core Component Technical Specification](../../../technical-specification.md)
