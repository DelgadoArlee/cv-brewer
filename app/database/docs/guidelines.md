# Database Component Coding Guidelines

## Database Service Code

- Service modules must be stored under `app/database/database_service/modules/<module-name>/`.
- Each module must own one application-level data responsibility.
- Service modules define application-level operations and must not contain database-specific queries, ORM models, or connection handling.

## Database Adapter Code

- Organize adapter repositories and ORM models by class or aggregate under `app/database/adapters/<adapter-name>/<class-name>/`, such as `app/database/adapters/sqlite/resume/`.
- Place the repository at the class directory root as `app/database/adapters/<adapter-name>/<class-name>/repository.py`.
- Place ORM models under the class directory as `app/database/adapters/<adapter-name>/<class-name>/models/<name-of-model>.py`.
- Repositories must own database access, ORM mapping, and transaction boundaries.
- Models must remain database-specific and must not leak into the Database Service or other components.
