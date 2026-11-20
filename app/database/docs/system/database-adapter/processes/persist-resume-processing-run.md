# Persist Resume Processing Run Technical Process

## 1. Purpose

Store a resume processing run record in SQLite and make stored run records available to callers through the Database Adapter.

## 2. Objective

Provide reliable persistence for resume processing run records, including embedded summary, performance, and error data, while preserving identifier references without resume-table relationships.

## 3. Scope

- Map Core resume processing run records to ORM models.
- Save run records in a transaction.
- Retrieve stored run records when requested by supported adapter operations.
- Translate database errors to adapter errors.

The process does not construct run records or control resume-processing workflow behavior.

## 4. Rules & Constraints

- All database operations must use an adapter session scope.
- Run records must be stored without changing their values.
- `resume_id` and `matched_resume_id` must be stored as identifier references without foreign-key relationships to resume tables.
- Embedded `summary`, `performance`, and `error` data must be persisted according to the SQLite schema mapping.
- Database failures must be translated to adapter errors.
- No resume data may be created, updated, or deleted.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    A([Start]) --> B{Operation}
    B -->|Save| C[Map run record to ORM model]
    C --> D[Add model in transaction]
    D --> E{Commit succeeded?}
    B -->|Read| F[Query stored run records]
    F --> G[Map ORM models to records]
    E -->|No| H[Translate adapter error]
    E -->|Yes| I([Complete])
    G --> I
    H --> J([Stop])
````

### Steps

1. Receive a save or read request for a resume processing run record.
2. For a save, map the Core run record to the ORM model and add it in a transaction.
3. For a read, query stored models and map them to Core run records.
4. Translate database errors to adapter errors.
5. Return the result.

## 6. Modules

- `app/database/adapters/sqlite/processing_log/repository.py` — Implements run and step persistence and retrieval operations.
- `app/database/adapters/sqlite/processing_log/models/resume_processing_run.py` — Defines the `resume_processing_runs` ORM model.
- `app/database/adapters/sqlite/engine.py` — Provides session scope handling.
- `app/database/adapters/sqlite/errors.py` — Translates database errors.

## 7. Data

- [Resume Processing Runs Table Schema](/app/database/docs/sqlite/schemas/resume-processing-runs.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Error Data Model](/docs/data/error.md)

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| PERSIST-RUN-001 | A complete run record with a `resume_id` reference. | The run is saved. | The record is retrievable unchanged and no resume relationship is required. |
| PERSIST-RUN-002 | A run record with embedded `error` data. | The run is saved. | Embedded error data is preserved. |
| PERSIST-RUN-003 | A run record without a saved resume. | The run is saved. | The record is stored with nullable `resume_id` as recorded. |

### 8.3 Test Coverage

Tests must verify save behavior, value preservation, and nullable/reference handling.

### 8.4 Test Organization

Tests reside under `tests/database/adapters/sqlite/processing_log/`.

### 8.5 Test Dependencies

Use a temporary SQLite database.

### 8.6 Testing Rules Compliance

Tests verify observable repository behavior using temporary storage.

## 9. References

- [Persist Resume Processing Run Process](/docs/system/database-service/processes/persist-resume-processing-run.md)
- [Database Adapter Technical System Specification](/app/database/docs/system/database-adapter/overview.md)
- [Resume Processing Run and Step Logging ADR](/docs/adr/Architecture/2026-11-19/resume-processing-run-logging.md)
