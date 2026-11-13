# Metadata Extraction Technical Process

## 1. Purpose

Define how the Core Processing Engine produces resume metadata and a content fingerprint from supplied file bytes.

## 2. Objective

- Capture the file name, size, and upload timestamp.
- Produce a stable fingerprint of the raw file content for deduplication.

## 3. Scope

### In Scope

- Building a resume metadata record from `ResumeInput`.
- Normalizing the upload timestamp.
- Calculating the content fingerprint.

### Out of Scope

- Reading file attributes from the file system.
- Duplicate detection and storage.
- PDF validation and parsing.

## 4. Rules & Constraints

- Use the supplied file name and bytes only.
- Set the file size to the byte length of the supplied content.
- Calculate the fingerprint as the SHA-256 hash of the raw bytes.
- Use the supplied upload timestamp when present.
- Convert timezone-aware timestamps to UTC and remove timezone information.
- Use the current UTC time when no upload timestamp is supplied.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    Start([ResumeInput]) --> Name[Read file name]
    Name --> Size[Calculate byte length]
    Size --> Time{Upload timestamp supplied?}
    Time -->|Yes| Normalize[Normalize to UTC without timezone]
    Time -->|No| Current[Use current UTC time]
    Normalize --> Fingerprint[Calculate SHA-256 fingerprint]
    Current --> Fingerprint
    Fingerprint --> Record[Return resume metadata]
````

### Steps

1. Receive the resume input.
2. Read the file name and calculate the content size.
3. Resolve the upload timestamp to a naive UTC value.
4. Calculate the SHA-256 fingerprint of the raw content.
5. Return the metadata record.

## 6. Modules

- `app/core/modules/metadata.py` — Builds metadata, normalizes timestamps, and calculates fingerprints.
- `app/core/pipeline/resume_processing.py` — Invokes metadata extraction before deduplication.
- `app/database/database_service/modules/resume/models.py` — Defines the resume metadata record.

## 7. Testing

### 7.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| RP-META-001 | A resume input with content and a file name. | Metadata is built. | Size and fingerprint match the supplied content. |
| RP-META-002 | A timezone-aware upload timestamp. | Metadata is built. | The timestamp is stored as naive UTC. |
| RP-META-003 | No upload timestamp. | Metadata is built. | The current UTC time is used. |
| RP-META-004 | Identical content in two inputs. | Metadata is built for both. | Both fingerprints are identical. |

## 8. References

- [Resume Processing Technical Process](resume-processing.md)
- [Resume Processing System Overview](../overview.md)
- [Core Component Technical Specification](../../../technical-specification.md)
- [User Resume Data Model](../../../../../../docs/data/user-resume.md)
