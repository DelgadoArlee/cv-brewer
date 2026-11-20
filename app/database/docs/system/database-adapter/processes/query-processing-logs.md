# Query Processing Logs Technical Process

## 1. Purpose

Query stored resume processing run and step models in SQLite and map them into application-level records for callers.

## 2. Objective

Provide all, recent, error-filtered, and per-run step list operations for processing logs using the existing adapter session and error-handling patterns without changing the stored schema.

## 3. Scope

- Query all stored processing run models.
- Query a caller-limited set of the newest processing run models by `started_at`.
- Query a caller-limited set of the newest error-indicating processing run models.
- Query the step models belonging to one run, with an optional caller-supplied limit.
- Map ORM models into Core processing run and step records.

The process does not create or finalize run or step records, construct records, or display them.

## 4. Rules & Constraints

- All database operations must use an adapter session scope.
- `list_runs()` must return every stored processing run record and keeps its existing behavior.
- `list_recent_runs(limit)` must return at most `limit` records ordered by `started_at` descending.
- `list_error_runs(limit)` must return at most `limit` records ordered by `started_at` descending where `status` is `FAILED`, `VALIDATION_FAILED`, or `PARTIAL_SUCCESS`, or an `error` object is present.
- `list_steps(run_id, *, limit=None)` must return the steps for one run; without a limit it must order by `step_order` and `attempt_number`, and with a limit it must return at most `limit` records ordered by `started_at` descending.
- Mapping must preserve all stored run and step values, including embedded `error` data.
- Database failures must be translated to adapter errors.
- No schema or migration changes are introduced by this process.
- The CLI must not access the database directly; queries must be reached through the Database Service and the adapter contract.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    A([Start]) --> B{Operation}
    B -->|list_runs| C[Query all run models]
    B -->|list_recent_runs| D[Apply started-at descending order and limit]
    B -->|list_error_runs| E[Apply error predicate, started-at descending order, and limit]
    B -->|list_steps| F{Steps limited?}
    F -->|No| G[Query run steps in step-order and attempt order]
    F -->|Yes| H[Apply started-at descending order and limit]
    C --> I[Map ORM models to Core records]
    D --> I
    E --> I
    G --> I
    H --> I
    I --> J([Return records])
    B -->|Database failure| K[Translate adapter error]
    K --> L([Stop])
````

### Steps

1. Receive a list request for one of the supported operations.
2. Open an adapter session and build the query for that operation.
3. For a capped query, order by the relevant timestamp descending and apply the caller-supplied limit.
4. For an error query, restrict results to error-indicating runs.
5. For a step query, restrict results to the requested run and use execution order unless a limit is supplied.
6. Map matching ORM models into Core run or step records and return them.
7. Translate database failures into adapter errors.

## 6. Modules

- `app/database/adapters/sqlite/processing_log/repository.py` — Implements run and step list operations.
- `app/database/adapters/sqlite/processing_log/models/resume_processing_run.py` — Defines the `resume_processing_runs` ORM model.
- `app/database/adapters/sqlite/processing_log/models/resume_processing_step.py` — Defines the `resume_processing_steps` ORM model.
- `app/database/adapters/sqlite/engine.py` — Provides session scope handling.
- `app/database/adapters/sqlite/errors.py` — Translates database errors.

## 7. Data

- [Resume Processing Runs Table Schema](/app/database/docs/sqlite/schemas/resume-processing-runs.md)
- [Resume Processing Steps Table Schema](/app/database/docs/sqlite/schemas/resume-processing-steps.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Error Data Model](/docs/data/error.md)

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| QUERY-PROC-001 | Several stored runs with different start times. | `list_runs()` is called. | All stored run records are returned. |
| QUERY-PROC-002 | Several stored runs with different start times. | `list_recent_runs(limit)` is called. | At most `limit` newest runs by `started_at` are returned. |
| QUERY-PROC-003 | Runs with success, failed, validation-failed, partial-success, and embedded-error states. | `list_error_runs(limit)` is called. | Only error-indicating runs are returned, newest first, up to `limit`. |
| QUERY-PROC-004 | Several steps for one run. | `list_steps(run_id)` is called. | All steps for that run are returned ordered by step order and attempt number. |
| QUERY-PROC-005 | Several steps for one run with different start times. | `list_steps(run_id, limit=limit)` is called. | At most `limit` newest steps by `started_at` are returned. |

### 8.3 Test Coverage

Tests must verify result ordering, limit enforcement, error filtering, run scoping, and value preservation.

### 8.4 Test Organization

Tests reside under `tests/database/adapters/sqlite/processing_log/`.

### 8.5 Test Dependencies

Use a temporary SQLite database.

### 8.6 Testing Rules Compliance

Tests verify observable repository behavior using temporary storage.

## 9. References

- [Query Processing Logs Process](/docs/system/database-service/processes/query-processing-logs.md)
- [Database Adapter Technical System Specification](/app/database/docs/system/database-adapter/overview.md)
