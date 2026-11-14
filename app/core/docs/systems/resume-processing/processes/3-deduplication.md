# Deduplication Technical Process

## 1. Purpose

Define how the Core Processing Engine detects resumes that were already stored with the same content.

## 2. Objective

- Prevent duplicate resume records from being processed and stored.
- Return the existing resume identifier when a duplicate is found.

## 3. Scope

### In Scope

- Querying the Database Service by content fingerprint.
- Returning a duplicate outcome for matching resumes.
- Reporting storage failures raised during the duplicate check.

### Out of Scope

- Fingerprint calculation.
- PDF validation, extraction, and parsing.
- Database query implementation and transactions.

## 4. Rules & Constraints

- Use the SHA-256 fingerprint produced during metadata extraction.
- Query the Database Service with `find_resume_by_content_fingerprint`.
- Return a duplicate outcome when a matching resume exists.
- Skip PDF validation, extraction, parsing, schema validation, and storage for duplicates.
- Report a storage failure when the duplicate check fails.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    Start([Content fingerprint]) --> Query[Find resume by fingerprint]
    Query -->|Failure| StorageFailure[Storage failure outcome]
    Query -->|No match| Continue[Continue processing]
    Query -->|Match| Duplicate[Duplicate outcome with resume ID]
````

### Steps

1. Receive the content fingerprint from metadata extraction.
2. Request the matching resume from the Database Service.
3. Return a duplicate outcome when a record exists.
4. Continue processing when no record exists.
5. Return a storage failure outcome when the lookup fails.

## 6. Modules

- `app/core/pipeline/resume_processing.py` — Coordinates the duplicate check and outcome.
- `app/core/services/resume/service.py` — Implements resume lookup by fingerprint.
- `app/core/services/resume/models.py` — Defines resume records.

## 7. Testing

### 7.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| RP-DEDUP-001 | A stored resume with the same fingerprint. | Deduplication runs. | A duplicate outcome with the existing resume ID is returned. |
| RP-DEDUP-002 | No stored resume with the fingerprint. | Deduplication runs. | Processing continues. |
| RP-DEDUP-003 | The Database Service lookup fails. | Deduplication runs. | A storage failure outcome is returned. |

## 8. References

- [Resume Processing Technical Process](resume-processing.md)
- [Resume Processing System Overview](../overview.md)
- [Core Component Technical Specification](../../../technical-specification.md)
