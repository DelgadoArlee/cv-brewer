# Persist Resume Processing Step Technical Process

## 1. Purpose

Store resume processing step records in SQLite and make stored step records available to callers through the Database Adapter.

## 2. Objective

Provide reliable persistence for step records associated with processing runs, preserving ordering, attempts, input/output summaries, duration, memory and CPU performance measurements, metadata, and embedded error data.

## 3. Scope

- Map Core resume processing step records to ORM models.
- Save step records in a transaction.
- Retrieve stored step records when requested by supported adapter operations.
- Enforce and preserve the run-to-step relationship.
- Translate database errors to adapter errors.

The process does not construct step records or execute processing steps.

## 4. Rules & Constraints

- All database operations must use an adapter session scope.
- Step records must be stored without changing their values.
- Each step record must reference an existing processing run through `run_id`.
- `(run_id, step_order, attempt_number)` must be preserved according to schema constraints.
- Embedded `input`, `output`, `performance`, `error`, and `metadata` data must be persisted according to the SQLite schema mapping.
- `input.source_step_id` must be stored as an identifier reference without a required foreign-key relationship.
- Database failures must be translated to adapter errors.
- No resume data or LLM activity log data may be created, updated, or deleted.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    A([Start]) --> B{Operation}
    B -->|Save| C[Map step record to ORM model]
    C --> D[Add model in transaction]
    D --> E{Commit succeeded?}
    B -->|Read| F[Query stored step records]
    F --> G[Map ORM models to records]
    E -->|No| H[Translate adapter error]
    E -->|Yes| I([Complete])
    G --> I
    H --> J([Stop])
````

### Steps

1. Receive a save or read request for a resume processing step record.
2. For a save, map the Core step record to the ORM model and add it in a transaction.
3. For a read, query stored models and map them to Core step records.
4. Translate database errors to adapter errors.
5. Return the result.

## 6. Modules

- `app/database/adapters/sqlite/processing_log/repository.py` — Implements run and step persistence and retrieval operations.
- `app/database/adapters/sqlite/processing_log/models/resume_processing_step.py` — Defines the `resume_processing_steps` ORM model.
- `app/database/adapters/sqlite/engine.py` — Provides session scope handling.
- `app/database/adapters/sqlite/errors.py` — Translates database errors.

## 7. Data

- [Resume Processing Steps Table Schema](/app/database/docs/sqlite/schemas/resume-processing-steps.md)
- [Resume Processing Runs Table Schema](/app/database/docs/sqlite/schemas/resume-processing-runs.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Error Data Model](/docs/data/error.md)

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| PERSIST-STEP-001 | A complete step record for an existing run. | The step is saved. | The record is retrievable unchanged and associated with the run. |
| PERSIST-STEP-002 | A step record with embedded `error`, `performance`, and `metadata` data. | The step is saved. | Embedded data is preserved. |
| PERSIST-STEP-003 | Multiple step records for the same run. | The steps are saved. | Ordering and attempt information are preserved for the run. |

### 8.3 Test Coverage

Tests must verify save behavior, run association, ordering/attempt preservation, and embedded data preservation.

### 8.4 Test Organization

Tests reside under `tests/database/adapters/sqlite/processing_log/`.

### 8.5 Test Dependencies

Use a temporary SQLite database.

### 8.6 Testing Rules Compliance

Tests verify observable repository behavior using temporary storage.

## 9. References

- [Persist Resume Processing Step Process](/docs/system/database-service/processes/persist-resume-processing-step.md)
- [Database Adapter Technical System Specification](/app/database/docs/system/database-adapter/overview.md)
- [Resume Processing Run and Step Logging ADR](/docs/adr/Architecture/2026-11-19/resume-processing-run-logging.md)
