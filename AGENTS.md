# AGENTS.md

## General Rules

- Never invent requirements, references, systems, or decisions.
- Obtain developer approval before changing requirements, architecture, design, or implementation behavior.
- Recommendations are allowed but are not approved decisions.
- Record significant architectural, technical, and design decisions in the appropriate ADR.
- If documentation contains conflicting or inconsistent information, report it and await developer direction before proceeding with affected work.
- Consult relevant component and module documentation before modifying or implementing them.
- Update relevant documentation after implementing or modifying a component or module.
- Read applicable documentation rules before creating or modifying documentation.
- Preserve existing document structures unless a change is necessary and approved.

## Implementation Rules

- A component must have Technical Specifcation document
- A component must be in architecture document and repositroy architecutre document.
- A system requires a High-Level System Document and Technical System Document before implementation. for non-database components only
- A module requires a Technical Module Document before implementation. for non-database components only
- A database table requires a Data Model Document and Technical Schema Document before implementation.
- Only modify files relevant to the requested task.
- Use `uv` as the package manager for all Python projects and dependency management.
- Do not use pip, poetry, or other package managers unless explicitly approved by the developer.

## Authoritative Documentation

- Requirements: `docs/requirements.md`
- Architecture: `docs/architecture.md`
- System Rules: `docs/system-rules.md`
- General Rules: `docs/rules/general-rules.md`
- Process Documentation: `docs/rules/process.md`
- High-Level System Documentation: `docs/rules/system.md`
- High-Level Feature Documentation: `docs/rules/feature.md`
- High-Level Data Model Documentation: `docs/rules/data.md`
- High-Level ADR: `docs/rules/adr.md`
- Component ADR: `docs/rules/component-adr.md`
- Technical System: `docs/rules/technical-system.md`
- Technical Module: `docs/rules/technical-spec.md`
- Tech Stack: `docs/tech-stack.md`
- Repository Architecture: `docs/repository/architecture.md`

## Verification

- No automated checks exist.
- Manually verify required section order, Mermaid code fences, and relative links when editing documentation.
- Ignore editor and tooling artifacts such as `.obsidian/`, `.DS_Store`, and `.aider*`.
