# AGENTS.md

## General Agent Rules

- Never invent requirements, references, systems, or decisions.
- Follow existing approved requirements, architecture, and design.
- Ask for approval before introducing or changing requirements, architecture, design, or implementation behavior.
- Minor implementation decisions that do not change approved behavior can proceed.- Recommendations are allowed but are not approved decisions.
- Record significant architectural, technical, and design decisions in the appropriate ADR.
- If documentation contains conflicting or inconsistent information, report it and await developer direction before proceeding with affected work.
- Consult relevant component and module documentation before modifying or implementing them.
- Update relevant documentation after implementing or modifying a component or module.
- Read applicable documentation rules before creating or modifying documentation.
- Preserve existing document structures unless a change is necessary and approved.

### Architecture Organization

CVBrewery uses four conceptual levels:

- Feature: Defines what the application should accomplish.
- System: Defines the technical responsibilities that support features.
- Process: Defines workflows that accomplish specific tasks within systems.
- Module: Defines encapsulated implementation units that can be shared or replaced.

### Architecture Organization Rules

- Follow the Feature → System → Process → Module model when organizing documentation.
- Features can involve multiple systems.
- Systems can support multiple features.
- Processes can coordinate multiple modules or systems.
- Modules can be shared across systems and processes.
- These levels represent logical responsibilities, not mandatory folder or package boundaries.
- Do not create unnecessary systems, processes, or modules.

## General Documentation Rules & Conventions

- Must read `docs/rules/general-rules.md` before writing or editing any type of document
- Follow the applicable documentation rules.
- If a required documentation format or convention is not defined, ask the developer before proceeding.

## Implementation Rules

- Components require a Technical Specification Document.
- Systems require High-Level System and Technical System Documents before implementation.
- Process require High-level Process and Technical Process Documents before implementation
- Modules require Technical Module Documents before implementation.
- Database tables require Data Model and Technical Schema Documents before implementation.
- System and Module documentation requirements apply only to non-database components.
- Only modify files relevant to the requested task.
- Use `uv` as the package manager for all Python projects and dependency management.
- Do not use pip, poetry, or other package managers unless explicitly approved by the developer.
- must conform with component architectural & design approaches stated in each components technical-specifcation.md

### Application Components

- CLI: `/cli`
- Core: `/core`
- Database: `/database`

## Implementation Workflow

1. Read the relevant documentation.
2. Identify the files required for the task.
3. Check for conflicting or missing requirements.
4. Ask for clarification or approval when necessary.
5. Implement the approved task.
6. Update relevant documentation.
7. Run tests if applicable
8. Manually verify the changes.

## Testing Strategy

- Testing Strategy: `docs/testing-strategy.md`

## Authoritative Documentation

    ### High-level Architecture & System Documentation
        - Requirements: `docs/requirements.md`
        - Architecture: `docs/architecture.md`
        - System Rules: `docs/system-rules.md`
        - Tech Stack: `docs/tech-stack.md`
        - Data models: `docs/data/`
        - High-level Feature documentation: `docs/features/`
        - High-level System documentation: `docs/system/`
        - High-level Process documentation: `docs/system/`
        - Repository Architecture: `docs/repository/architecture.md`

    ### Low-level Component Documentation (Technical & Implementation):
        - Technical Specification Document: `<component>/docs/technical-specification.md`
        - Technical System Documentation: `<component>/docs/systems/<system-name>/`
        - Technical Process Documentation: `<component>/docs/systems/<system-name>/processes/<process-name>.md
        - Technical Module Documentation: `<component>/docs/modules/<module-name>.md`
        - Technical Schema Documentation: `<component>/docs/schemas/<schema-name>.md`

    ### Database-specific Documentation
       - Database service specific documentation & schemas: `database/docs/<database-service-name>/`

## Verification

- No automated checks exist.
- Manually verify required section order, Mermaid code fences, and relative links when editing documentation.
- Ignore editor and tooling artifacts such as `.obsidian/`, `.DS_Store`, and `.aider*`.
- Do not claim verification was successful unless it was actually performed.
- Report checks that could not be performed.
