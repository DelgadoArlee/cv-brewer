# Query LLM Logs Technical Process

## 1. Purpose

Query stored LLM activity log models in SQLite and map them into application-level records for callers.

## 2. Objective

Provide all, recent, and error-filtered list operations for LLM activity logs using the existing adapter session and error-handling patterns without changing the stored schema.

## 3. Scope

- Query all stored LLM log models.
- Query a caller-limited set of the newest LLM log models by `created_at`.
- Query a caller-limited set of the newest error-indicating LLM log models.
- Map ORM models into Core LLM log records.

The process does not save records, build log records, or display them.

## 4. Rules & Constraints

- All database operations must use an adapter session scope.
- `list_all()` must return every stored LLM log record and keeps its existing behavior.
- `list_recent(limit)` must return at most `limit` records ordered by `created_at` descending.
- `list_errors(limit)` must return at most `limit` records ordered by `created_at` descending where `status` is `FAILED` or `TIMEOUT`, or `error_type` is not null, or `error_message` is not null.
- Mapping must preserve all stored record values.
- Database failures must be translated to adapter errors.
- No schema or migration changes are introduced by this process.
- The CLI must not access the database directly; queries must be reached through the Database Service and the adapter contract.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    A([Start]) --> B{Operation}
    B -->|list_all| C[Query all LLM log models]
    B -->|list_recent| D[Apply created-at descending order and limit]
    B -->|list_errors| E[Apply error predicate, created-at descending order, and limit]
    C --> F[Map ORM models to Core records]
    D --> F
    E --> F
    F --> G([Return records])
    B -->|Database failure| H[Translate adapter error]
    H --> I([Stop])
````

### Steps

1. Receive a list request for one of the supported operations.
2. Open an adapter session and build the query for that operation.
3. For a capped query, order by the relevant timestamp descending and apply the caller-supplied limit.
4. For an error query, restrict results to error-indicating records.
5. Map matching ORM models into Core records and return them.
6. Translate database failures into adapter errors.

## 6. Modules

- `app/database/adapters/sqlite/llm_log/repository.py` — Implements all, recent, and error-filtered list operations.
- `app/database/adapters/sqlite/llm_log/models/llm_log.py` — Defines the `llm_logs` ORM model.
- `app/database/adapters/sqlite/engine.py` — Provides session scope handling.
- `app/database/adapters/sqlite/errors.py` — Translates database errors.

## 7. Data

- [LLM Logs Table Schema](/app/database/docs/sqlite/schemas/llm-logs.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| QUERY-LOG-001 | Several stored logs with different creation times. | `list_all()` is called. | All stored records are returned. |
| QUERY-LOG-002 | Several stored logs with different creation times. | `list_recent(limit)` is called. | At most `limit` newest records by `created_at` are returned. |
| QUERY-LOG-003 | Stored logs with success, failed, timeout, and error-detail records. | `list_errors(limit)` is called. | Only error-indicating records are returned, newest first, up to `limit`. |
| QUERY-LOG-004 | No stored logs. | A list operation is called. | An empty list is returned. |

### 8.3 Test Coverage

Tests must verify result ordering, limit enforcement, error filtering, and value preservation.

### 8.4 Test Organization

Tests reside under `tests/database/adapters/sqlite/llm_log/`.

### 8.5 Test Dependencies

Use a temporary SQLite database.

### 8.6 Testing Rules Compliance

Tests verify observable repository behavior using temporary storage.

## 9. References

- [Query LLM Logs Process](/docs/system/database-service/processes/query-llm-logs.md)
- [Database Adapter Technical System Specification](/app/database/docs/system/database-adapter/overview.md)
