# Database Component Architecture Decision Log

This log indexes the component-level Architecture Decision Records (ADRs) for the database component. Entries are ordered with the newest decisions first.

| Date | Decision | Status |
| --- | --- | --- |
| 2026-11-13 | [Retain Database Adapters as the Database Component Boundary](11-13-26/adapter-only-boundary.md) — Keep adapters in Database, implement Core-owned repository contracts, and preserve the resume persistence schema. | Accepted |
| 2026-11-10 | [Establish resume persistence](11-10-26/resume-persistence.md) — Use a hybrid relational resume schema, unique content fingerprints, service-layer resume operations, and SQLite adapter repositories and models. | Superseded |
| 2026-11-06 | [Establish SQLite adapter foundation](11-06-26/sqlite-adapter-foundation.md) — Use synchronous SQLAlchemy, explicit SQLite URLs, adapter-local errors, and self-contained Alembic scaffolding. | Accepted |
