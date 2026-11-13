# Persist Resume Process Document

## 1. Purpose / Summary

This process stores a complete application-level resume record in the configured database implementation. It preserves the resume hierarchy and ordering, enforces storage constraints, completes the operation atomically, and reports a storage failure when persistence does not succeed.

## 2. Process Flow

```` mermaid
flowchart TD
    A([Start]) --> B[Receive resume record]
    B --> C[Persist resume and ordered child data]
    C --> D{Storage operation succeeds?}
    D -->|Yes| E([Complete persistence])
    D -->|No| F[Undo partial changes]
    F --> G([Report storage failure])
````

## 3. Rules

- **must** persist the complete resume record, including all child data
- **must** preserve child data order
- **must** enforce unique content fingerprints
- **must** maintain the relationship between a resume and its child records
- **must** complete a successful persistence operation atomically
- **must** undo partial changes when persistence fails
- **must** report storage failures to the caller

## 4. Constraints

- The process does not decide when resume data is valid for storage.
- The process does not expose database-specific implementation details to callers.
- The process does not define application-level resume operations.

## 5. References

- [Database Adapter System Overview](../overview.md)
- [User Resume Data Model](../../../data/user-resume.md)
- [Persist Resume Technical Process](../../../../app/database/docs/systems/database-adapter/processes/persist-resume.md)
