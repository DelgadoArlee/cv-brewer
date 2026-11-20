# LLM Activity Logging Feature Overview

## 1. Purpose / Summary

The LLM activity logging feature records language-model generation activity so completed calls, failures, usage, performance, and errors can be reviewed later. It provides a read-only review path that generates HTML reports and is separate from resume creation and other application workflows.

## 2. Objective

- Record structured generation activity without changing language-model call behavior.
- Keep non-LLM application activity out of the activity log.
- Provide token usage, timing, memory, status, and error details for each recorded call.
- Persist records so they remain available after the originating application session ends.
- Let reviewers generate standalone HTML reports for stored LLM activity through a dedicated entry point.
- Let reviewers include LLM activity in error and combined HTML log reports alongside processing runs.

## 3. User Journey

````mermaid
flowchart TD
    A[User starts an application workflow] --> B[Workflow requests structured generation]
    B --> C[Language-model call completes]
    C --> D[System records the call outcome]
    D --> E[System stores the activity record]
    E --> F{Record available?}
    F -->|Yes| G[User opens the logger CLI]
    F -->|No| N[Original workflow continues unchanged]
    G --> H{Log database available?}
    H -->|No| M[System reports no database]
    H -->|Yes| I[User selects a log database]
    I --> K[User selects a log view]
    K --> L[System generates an HTML report with matching LLM activity logs]
````

## 4. Systems

| System | Description |
| --- | --- |
| [LLM Adapter System](/docs/system/llm-adapter/overview.md) | Observes language-model calls and reports their outcome for logging. |
| [LLM Logger System](/docs/system/llm-logger/overview.md) | Builds application-level LLM activity records from observed calls. |
| [Logger Service System](/docs/system/logger-service/overview.md) | Delivers log records to configured destinations. |
| [Database Service System](/docs/system/database-service/overview.md) | Stores and retrieves LLM activity records. |

## 5. References

- [LLM Activity Logging Decision](/docs/adr/Architecture/2026-11-19/llm-activity-logging.md)
- [Render Logger Reports as HTML](/docs/adr/Architecture/2026-11-20/html-log-reports.md)
- [Expand Logger CLI Log Views](/docs/adr/Architecture/2026-11-20/logger-cli-log-views.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)
- [Logger CLI Process](/docs/system/logger-cli.md)
- [Log Generation Call Process](/docs/system/llm-adapter/processes/log-generation-call.md)
- [Record LLM Call Process](/docs/system/llm-logger/processes/record-llm-call.md)
- [Emit Log Entry Process](/docs/system/logger-service/processes/emit-log-entry.md)
- [Persist LLM Log Process](/docs/system/database-service/processes/persist-llm-log.md)
- [Query LLM Logs Process](/docs/system/database-service/processes/query-llm-logs.md)

## 6. Acceptance Criteria

**Given:** A structured generation call completes successfully<br>
**When:** The activity is recorded<br>
**Then:** A log with `SUCCESS` status, response details, usage, timing, and memory information is available.

**Given:** A structured generation call fails or times out<br>
**When:** The activity is recorded<br>
**Then:** A log with `FAILED` or `TIMEOUT` status and error details is available, and the original error is unchanged.

**Given:** A non-LLM application operation completes<br>
**When:** Application activity is reviewed<br>
**Then:** No LLM activity log is created for that operation.

**Given:** Stored LLM activity logs exist<br>
**When:** A reviewer opens the logger CLI and selects `llm`<br>
**Then:** The available records are included in a generated HTML report.

**Given:** Multiple environment databases exist<br>
**When:** A reviewer opens the logger CLI and selects a log database<br>
**Then:** The records from the selected database are included in the selected HTML log report.

**Given:** Stored LLM activity logs exist<br>
**When:** A reviewer selects `error` or `all`<br>
**Then:** LLM records are included with processing run records in the HTML report according to that view's rules.

**Given:** An environment database does not exist<br>
**When:** A reviewer opens the logger CLI<br>
**Then:** That environment is not offered for selection.

**Given:** Logging is unavailable during a language-model call<br>
**When:** The call completes or fails<br>
**Then:** The request, response, and propagated error are unchanged.
