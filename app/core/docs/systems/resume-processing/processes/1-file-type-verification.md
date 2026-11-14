# File Type Verification Technical Process

## 1. Purpose

Define how the Core Processing Engine verifies that supplied content is a PDF before further processing.

## 2. Objective

- Confirm the supplied bytes begin with the PDF signature.
- Reject non-PDF content before metadata extraction, deduplication, or PDF parsing.

## 3. Scope

### In Scope

- Signature verification on supplied file bytes.
- Raising an invalid file type error for non-PDF content.

### Out of Scope

- PDF encryption, structure, and page validation.
- Text extraction and parsing.
- File-system access.

## 4. Rules & Constraints

- Operate on the supplied bytes only.
- Require the content to start with `%PDF-`.
- Reject content that does not match the signature.
- Do not inspect the file extension or file name.
- Do not validate PDF structure in this process.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    Start([Resume bytes]) --> Check{Starts with %PDF-?}
    Check -->|Yes| Continue[Continue processing]
    Check -->|No| Reject[Raise invalid file type error]
````

### Steps

1. Receive the resume bytes from the processing pipeline.
2. Compare the beginning of the bytes with the PDF signature.
3. Continue when the signature matches.
4. Raise an invalid file type error when the signature does not match.

## 6. Modules

- `app/core/services/pdf/service.py` — Implements PDF signature verification.
- `app/core/pipeline/resume_processing.py` — Invokes verification as the first stage.

## 7. Testing

### 7.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| RP-FTV-001 | Content beginning with `%PDF-`. | The file type is verified. | Verification succeeds. |
| RP-FTV-002 | Content without the PDF signature. | The file type is verified. | An invalid file type error is raised. |
| RP-FTV-003 | Empty content. | The file type is verified. | An invalid file type error is raised. |

## 8. References

- [Resume Processing Technical Process](resume-processing.md)
- [Resume Processing System Overview](../overview.md)
- [Core Component Technical Specification](../../../technical-specification.md)
