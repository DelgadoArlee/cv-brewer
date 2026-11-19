# Emit Log Entry Technical Process

## 1. Purpose

Deliver a structured log record to every configured sink.

## 2. Objective

Ensure each accepted record is forwarded unchanged so destinations receive consistent data.

## 3. Scope

- Accept a log record.
- Forward the record to each configured sink.
- Report delivery failures.

The process does not build records or implement destinations.

## 4. Rules & Constraints

- Records must be passed to sinks without modification.
- All configured sinks must receive the record even if another sink fails.
- A sink failure must be reported after delivery is attempted.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B[Receive log record]
    B --> C{For each configured sink}
    C --> D[Deliver record]
    D --> E{Delivery succeeded?}
    E -->|No| F[Record failure]
    E -->|Yes| G{More sinks?}
    F --> G
    G -->|Yes| C
    G -->|No| H{Failures recorded?}
    H -->|Yes| I[Report failure]
    H -->|No| J([Complete])
    I --> K([Stop])
````

### Steps

1. Receive the log record.
2. Iterate over configured sinks.
3. Deliver the unchanged record to each sink.
4. Record any delivery failure and continue with remaining sinks.
5. Report an error when any sink failed; otherwise complete.

## 6. Modules

- `app/core/services/logger/service.py` — Implements the logging service and delivery loop.
- `app/core/services/logger/port.py` — Defines the sink contract.
- `app/core/services/logger/models.py` — Defines the generic log record.

## 7. Testing

### 7.1 Test Level

Process level.

### 7.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| LOG-001 | One sink configured. | A record is emitted. | The sink receives the unchanged record. |
| LOG-002 | Several sinks configured. | A record is emitted. | Every sink receives the record. |
| LOG-003 | No sinks configured. | A record is emitted. | The operation completes without error. |
| LOG-004 | A sink raises an error. | A record is emitted. | Remaining sinks are attempted and the error is reported. |

### 7.3 Test Coverage

Tests must verify unchanged delivery and failure handling.

### 7.4 Test Organization

Tests reside under `tests/core/services/logger/`.

### 7.5 Test Dependencies

Use in-memory test doubles for log sinks.

### 7.6 Testing Rules Compliance

Tests verify observable delivery behavior without depending on a destination implementation.

## 8. References

- [Logger Service Technical System Specification](/app/core/docs/system/logger-service/overview.md)
- [Emit Log Entry Process](/docs/system/logger-service/processes/emit-log-entry.md)
