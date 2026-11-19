# Persist LLM Log Technical Process

## 1. Purpose

Store an LLM activity log record in SQLite and return stored records to callers.

## 2. Objective

Provide reliable save and list operations for LLM activity logs using the existing adapter transaction and error handling patterns.

## 3. Scope

- Map Core LLM log records to ORM models.
- Save records in a transaction.
- List stored records.
- Translate database errors to adapter errors.

The process does not build log records or display them.

## 4. Rules & Constraints

- All database operations must use an adapter session scope.
- Records must be stored without changing their values.
- Database failures must be translated to adapter errors.
- No resume data may be created, updated, or deleted.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B{Operation}
    B -->|Save| C[Map record to ORM model]
    C --> D[Add model in transaction]
    D --> E{Commit succeeded?}
    B -->|List| F[Query stored records]
    F --> G[Map ORM models to records]
    E -->|No| H[Translate adapter error]
    E -->|Yes| I([Complete])
    G --> I
    H --> J([Stop])
````

### Steps

1. Receive a save or list request.
2. For a save, map the Core record to the ORM model and add it in a transaction.
3. For a list, query stored models and map them to Core records.
4. Translate database errors to adapter errors.
5. Return the result.

## 6. Modules

- `app/database/adapters/sqlite/llm_log/repository.py` — Implements save and list operations.
- `app/database/adapters/sqlite/llm_log/models/llm_log.py` — Defines the `llm_logs` ORM model.
- `app/database/adapters/sqlite/engine.py` — Provides session scope handling.
- `app/database/adapters/sqlite/errors.py` — Translates database errors.

## 7. Data

- [LLM Logs Table Schema](/app/database/docs/sqlite/schemas/llm-logs.md)

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| PERSIST-LOG-001 | A complete log record. | The record is saved. | The record is retrievable unchanged. |
| PERSIST-LOG-002 | No saved records. | Logs are listed. | An empty list is returned. |
| PERSIST-LOG-003 | Several saved records. | Logs are listed. | All records are returned. |

### 8.3 Test Coverage

Tests must verify save, list, and value preservation.

### 8.4 Test Organization

Tests reside under `tests/database/adapters/sqlite/llm_log/`.

### 8.5 Test Dependencies

Use a temporary SQLite database.

### 8.6 Testing Rules Compliance

Tests verify observable repository behavior using temporary storage.

## 9. References

- [Persist LLM Log Process](/docs/system/database-service/processes/persist-llm-log.md)
- [Database Adapter Technical System Specification](/app/database/docs/system/database-adapter/overview.md)
