# Store Resume Process Document

## 1. Purpose / Summary

This process stores a complete resume record through the Database Service so that validated resume data can be retrieved later. It ensures each stored resume has a stable identity and creation time, delegates persistence to the configured database adapter, and reports a stored record or a persistence failure.

## 2. Process Flow

    ```` mermaid
    flowchart TD
        A([Start]) --> B[Receive resume data]
        B --> C{Resume identifier provided?}
        C -->|No| D[Assign unique identifier]
        C -->|Yes| E[Keep provided identifier]
        D --> F{Creation time provided?}
        E --> F
        F -->|No| G[Assign creation time]
        F -->|Yes| H[Keep provided creation time]
        G --> I[Persist complete resume record]
        H --> I
        I --> J{Persisted successfully?}
        J -->|Yes| K([Return stored record])
        J -->|No| L([Report persistence failure])
    ````

## 3. Rules

- **must** assign a unique identifier when the received resume data does not provide one
- **must** assign a creation time when the received resume data does not provide one
- **must** preserve provided identifiers and creation times
- **must** persist the complete resume record, including ordered child data
- **must** report persistence failures to the caller
- **must** report duplicate content fingerprints as persistence failures
- **must** not perform resume validation or parsing as part of this process

## 4. Constraints

- The process does not decide whether uploaded files satisfy processing requirements.
- The process does not manage input files or file-system operations.
- The process does not define resume deletion behavior.

## 5. References

- [Database Service System Overview](../overview.md)
- [User Resume Data Model](../../../data/user-resume.md)
- [Store Resume Technical Process](../../../../database/docs/systems/database-service/processes/store-resume.md)
