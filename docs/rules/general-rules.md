Documentation Rules and Conventions

1. General Conventions

- All documentation must be written in Markdown (.md).
- Use kebab-case for file and folder naming.
- Follow the appropriate formatting rules defined in docs/rules/.
- Keep documentation simple, concise, and consistent.
- Always use quadruple backticks for Markdown code blocks.
- use absolute paths when referencing

2. Documentation Structure

- docs/ contains high-level documentation:
  - Features and systems.
  - Data models and schemas.
  - Documentation rules, conventions, and implementation guidelines.
  - Repository and release documentation.
- <component>/docs/ contains implementation-specific and technical documentation for the component.

3. System Documentation

- docs/system/ contains high-level system documentation.
- <component>/docs/system/ contains low-level, technical, and component-specific system documentation.
- Technical System Documents must reference their corresponding High-Level System Documents.

1. Process Documentation

- Application-level processes should be documented separately from System-specific processes.
- System-Level Processes: Document processes under `docs/systems/<system-name>/processes/` to indicate which System they belong to.
- Application-Level Processes: Document processes under `docs/processes/` when they support the overall application and do not belong to a specific System.

5. Data Schema Documentation

- Data schemas must have separate documentation.
- Non-database schemas → component documentation. `<component>/docs/schemas/<data-name>.md`
- Database schemas → responsible database service documentation. `database/docs/<name-of-db-service>/schemas/<data-name>`.md:
- Database schema documentation must be maintained within the documentation of the database service responsible for storing the data.

6. Database Documentation Rules

- Each database service must have its own documentation directory.
- Each database service must have its own documentation directory:
  - `database/docs/<database-service-name>/`
- Database-specific schemas must be documented under their corresponding database:
  - `database/docs/<database-service-name>/schemas/<schema-name>.md`
- Database schema documentation must follow the Database Schema Documentation Rules.

7. Documentation rules & conventions

- Process Documentation rules: `docs/rules/process.md`
- High-Level ADR rules: `docs/rules/adr.md`
- Component ADR rules: `docs/rules/component-adr.md`
- High-Level Feature Documentation rule: `docs/rules/feature.md`
- High-Level System Documentation rules: `docs/rules/system.md`
- High-level Process Documentation rules: `docs/rules/process.md`
- High-Level Data Model Documentation rules: `docs/rules/data.md`
- Technical System rules: `docs/rules/technical-system.md`
- Technical Process rules: `docs/rules/technical-process.md`
- Component Technical Specification rules: `docs/rules/technical-spec.md`
- Database Documentation rules: `docs/rules/database`

8. Testing Documentation

- The testing component must not have component documentation.
- The tests themselves are the documentation for the testing component.
