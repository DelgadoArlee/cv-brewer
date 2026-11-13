# Load Resume Process Document

## 1. Purpose / Summary

This process retrieves stored resume data from the configured database implementation and returns complete application-level resume records. It supports lookup by identifier, lookup by content fingerprint, and listing stored resumes while preserving child data order.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B[Receive lookup request]
    B --> C[Retrieve stored resume data]
    C --> D{Single record found?}
    D -->|Yes| E[Assemble complete resume record]
    D -->|No| F{Listing requested?}
    F -->|Yes| G[Assemble stored resume records]
    F -->|No| H([Return no matching record])
    E --> I([Return resume record])
    G --> J([Return resume records])
````

## 3. Rules

- **must** retrieve resume data by identifier or content fingerprint
- **must** support listing all stored resumes
- **must** return complete application-level resume records with ordered child data
- **must** return no matching record when a single-record lookup does not find a result
- **must** report retrieval failures to the caller
- **must** not expose database-specific implementation details to callers

## 4. Constraints

- The process does not define application-level operation behavior.
- The process does not validate, parse, or modify stored resume data.
- The process does not define resume deletion behavior.

## 5. References

- [Database Adapter System Overview](../overview.md)
- [User Resume Data Model](../../../data/user-resume.md)
- [Load Resume Technical Process](../../../../app/database/docs/systems/database-adapter/processes/load-resume.md)
