# Store Resume Technical Process

## 1. Purpose

Create a stored resume record from application-level resume data and delegate persistence to the configured resume repository.

## 2. Objective

Store a complete resume record with a unique identifier, creation timestamp, ordered child data, and validation metadata.

## 3. Scope

- Receive application-level resume data.
- Generate missing identifiers and timestamps.
- Delegate persistence to the resume repository.
- Return the stored resume record.

The process does not validate resume content or perform database access directly.

## 4. Rules & Constraints

- A resume identifier must be generated with `uuid4` when absent.
- A creation timestamp must be generated when absent.
- Provided identifiers and timestamps must be preserved.
- Child data order must be preserved in the record passed to the adapter.
- Persistence failures must be propagated to the caller.
- The process must not import or call SQLAlchemy or SQLite.

## 5. Workflow

### Diagram

```` mermaid
    flowchart TD
        A([Start]) --> B[Receive resume data]
        B --> C{Resume ID provided?}
        C -->|No| D[Generate UUID]
        C -->|Yes| E[Keep resume ID]
        D --> F{Created at provided?}
        E --> F
        F -->|No| G[Generate timestamp]
        F -->|Yes| H[Keep timestamp]
        G --> I[Build stored resume record]
        H --> I
        I --> J[Delegate save to repository]
        J --> K{Saved?}
        K -->|Yes| L([Return stored record])
        K -->|No| M([Propagate failure])
````

### Steps

1. Receive the application-level resume data.
2. Use the provided resume identifier or generate a new UUID.
3. Use the provided creation timestamp or generate one.
4. Build a stored resume record.
5. Delegate the save operation to the resume repository.
6. Return the stored record or propagate the adapter failure.

## 6. Modules

- [Resume Service Module](../../../modules/database-service/resume/service.md) — Defines the service operation and generated resume fields.
- [Resume Repository Module](../../../modules/database-service/resume/repository.md) — Defines the persistence contract.
- [Resume Models Module](../../../modules/database-service/resume/models.md) — Defines resume records.

## 7. Data

- [User Resume Data Model](../../../../../docs/data/user-resume.md) — Source structure for resume records.

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| STORE-001 | Resume data without an ID or timestamp. | Save is called. | The returned record has a UUID and creation timestamp. |
| STORE-002 | Resume data with an ID and timestamp. | Save is called. | The provided values are preserved. |
| STORE-003 | A repository that rejects the save. | Save is called. | The failure is propagated. |

### 8.3 Test Coverage

Tests must verify observable service behavior and failure propagation.

## 9. References

- [Database Service Technical System Specification](../overview.md)
- [Database Service System Overview](../../../../../docs/system/database-service/overview.md)
- [Resume Persistence ADR](../../../adr/11-10-26/resume-persistence.md)
