# PDF Validation Technical Process

## 1. Purpose

Define how the Core Processing Engine rejects encrypted, structurally invalid, or empty PDF documents.

## 2. Objective

- Confirm the PDF can be opened and has at least one page.
- Reject encrypted or password-protected PDFs.
- Reject PDFs with an invalid page structure.

## 3. Scope

### In Scope

- Opening the PDF from supplied bytes.
- Encryption and page-count validation.
- Raising invalid PDF errors.

### Out of Scope

- PDF signature verification.
- Text extraction and readability checks.
- File-system access.

## 4. Rules & Constraints

- Operate on the supplied bytes only.
- Reject encrypted or password-protected PDFs.
- Reject PDFs whose page structure cannot be read.
- Reject PDFs with zero pages.
- Do not extract text in this process.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    Start([PDF bytes]) --> Open{PDF opens?}
    Open -->|No| Invalid[Raise invalid PDF error]
    Open -->|Yes| Encrypted{Encrypted?}
    Encrypted -->|Yes| Invalid
    Encrypted -->|No| Pages{Pages readable and present?}
    Pages -->|No| Invalid
    Pages -->|Yes| Continue[Continue processing]
````

### Steps

1. Open the PDF from the supplied bytes.
2. Reject the document when it cannot be opened.
3. Reject the document when it is encrypted or password-protected.
4. Read the page count and reject unreadable page structures.
5. Reject the document when it contains no pages.
6. Continue processing when validation succeeds.

## 6. Modules

- `core/src/core/modules/pdf_processing.py` — Implements PDF opening, encryption, and page validation.
- `core/src/core/pipeline/resume_processing.py` — Invokes PDF validation after deduplication.
- `core/src/core/errors.py` — Defines the invalid PDF error.

## 7. Testing

### 7.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| RP-PDF-001 | A valid PDF with at least one page. | PDF validation runs. | Validation succeeds. |
| RP-PDF-002 | An encrypted PDF. | PDF validation runs. | An invalid PDF error is raised. |
| RP-PDF-003 | A PDF with an invalid structure. | PDF validation runs. | An invalid PDF error is raised. |
| RP-PDF-004 | A PDF with zero pages. | PDF validation runs. | An invalid PDF error is raised. |

## 8. References

- [Resume Processing Technical Process](resume-processing.md)
- [Resume Processing System Overview](../overview.md)
- [Core Component Technical Specification](../../../technical-specification.md)
