# Retrieve Resume Process Document

## 1. Purpose / Summary

This process retrieves stored resume records through the Database Service by identifier, by content fingerprint, or as a complete list. It returns complete resume records when found and reports no matching record when a single-record lookup does not succeed.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B{Requested lookup}
    B -->|By identifier| C[Retrieve resume by identifier]
    B -->|By content fingerprint| D[Retrieve resume by content fingerprint]
    B -->|List all| E[Retrieve all stored resumes]
    C --> F{Record found?}
    D --> F
    F -->|Yes| G([Return complete resume record])
    F -->|No| H([Return no matching record])
    E --> I([Return stored resume records])
````

## 3. Rules

- **must** support retrieval by resume identifier
- **must** support retrieval by content fingerprint
- **must** support listing all stored resumes
- **must** return a complete resume record, including ordered child data, when a match is found
- **must** return no matching record when a single-record lookup does not find a result
- **must** report retrieval failures to the caller
- **must** not treat a missing resume record as a system failure

## 4. Constraints

- The process does not validate, parse, or modify stored resume data.
- The process does not define resume deletion behavior.
- The process does not expose database-specific implementation details to callers.

## 5. References

- [Database Service System Overview](../overview.md)
- [User Resume Data Model](../../../data/user-resume.md)
- [Retrieve Resume Technical Process](../../../../app/database/docs/systems/database-service/processes/retrieve-resume.md)
