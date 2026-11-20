# Database Component Architecture Decision Log

This log indexes the component-level Architecture Decision Records (ADRs) for the database component. Entries are ordered with the newest decisions first.

| Date | Decision | Status | High-Level ADR |
| --- | --- | --- | --- |
| 2026-11-19 | [Persist resume processing runs and steps in SQLite](/app/database/docs/adr/11-19-26/resume-processing-run-step-persistence.md) — Add `resume_processing_runs` and `resume_processing_steps` tables with a one-to-many relationship, embedded structured fields, and resume identifier references without foreign-key relationships. | Accepted | [Resume Processing Run and Step Logging](/docs/adr/Architecture/2026-11-19/resume-processing-run-logging.md) |
| 2026-11-19 | [Persist LLM activity logs in SQLite](/app/database/docs/adr/11-19-26/llm-log-persistence.md) — Add an `llm_logs` table with an optional processing step reference, Alembic migration, and save/list repository implementing a Core-owned contract. | Accepted | [LLM Activity Logging](/docs/adr/Architecture/2026-11-19/llm-activity-logging.md) |
| 2026-11-13 | [Retain Database Adapters as the Database Component Boundary](/app/database/docs/adr/11-13-26/adapter-only-boundary.md) — Keep adapters in Database, implement Core-owned repository contracts, and preserve the resume persistence schema. | Accepted | [Database Service in Core](/docs/adr/Architecture/2026-11-13/database-service-to-core.md) |
| 2026-11-10 | [Establish resume persistence](/app/database/docs/adr/11-10-26/resume-persistence.md) — Use a hybrid relational resume schema, unique content fingerprints, service-layer resume operations, and SQLite adapter repositories and models. | Superseded | [Database Persistence](/docs/adr/Architecture/2026-11-04/database-persistence.md) |
| 2026-11-06 | [Establish SQLite adapter foundation](/app/database/docs/adr/11-06-26/sqlite-adapter-foundation.md) — Use synchronous SQLAlchemy, explicit SQLite URLs, adapter-local errors, and self-contained Alembic scaffolding. | Accepted | [Database Persistence](/docs/adr/Architecture/2026-11-04/database-persistence.md) |
