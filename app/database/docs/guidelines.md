# Database Component Coding Guidelines

## Database Adapter Code

- Organize adapter repositories and ORM models by class or aggregate under `app/database/adapters/<adapter-name>/<class-name>/`, such as `app/database/adapters/sqlite/resume/`.
- Place the repository at the class directory root as `app/database/adapters/<adapter-name>/<class-name>/repository.py`.
- Place ORM models under the class directory as `app/database/adapters/<adapter-name>/<class-name>/models/<name-of-model>.py`.
- Repositories must implement Core-owned repository contracts.
- Repositories must own database access, ORM mapping, and transaction boundaries.
- Models must remain database-specific and must not leak into the Core services or other components.
- Adapters must not define application-level operations or application-level record structures.
