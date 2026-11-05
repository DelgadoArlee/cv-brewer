Documentation Rules and Conventions

1. General Conventions

- All documentation must be written in Markdown (.md).
- Use kebab-case for file and folder naming.
- Follow the appropriate formatting rules defined in docs/rules/.
- Keep documentation simple, concise, and consistent.
- code block must always be in quadruple backticks (````).

3. Documentation Structure

- docs/ contains high-level documentation:
  - Features and systems.
  - Data models and schemas.
  - Documentation rules, conventions, and implementation guidelines.
  - Repository and release documentation.
- <component>/docs/ contains implementation-specific and technical documentation for the component.

4. System Documentation

- docs/system/ contains high-level system documentation.
- <component>/docs/system/ contains low-level, technical, and component-specific system documentation.
- Technical System Documents must reference their corresponding High-Level System Documents.

5. Data Schema Documentation

- Data schemas must have separate documentation.
- Schemas that are not stored in a database must be documented in:
  - <component>/docs/schemas/<data-name>.md
- Schemas that are stored in a database must be documented in:
  - database/docs/<name-of-db-service>/schemas/<data-name>.md
- Database schema documentation must be maintained within the documentation of the database service responsible for storing the data.
