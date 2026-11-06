# Technical Specification Format Rules

## 1. Purpose

This document defines the formatting standards for Technical Specification documents within CVBrewery.

Technical Specifications describe the technical organization, structure, design approaches, constraints, and deployment considerations of individual components.

## 2. Document Structure

All Technical Specification documents must follow this structure:

1. Purpose
2. Objective
3. Scope
4. Rules & Constraints
5. Architectural & Design Approaches
6. Systems
7. File Structure
8. Deployment (Optional)
9. References

## 3. Section Guidelines

### 3.1. Purpose

Describes the purpose of the document and what it aims to document.

### 3.2. Objective

Defines the technical goals and intended outcomes of the component.

### 3.3. Scope

Defines the technical boundaries of the component.

Clearly identify what is included and excluded from the specification.

### 3.4. Rules & Constraints

Lists the technical rules, limitations, and constraints that must be followed when designing, developing, and maintaining the component.

### 3.5. Architectural & Design Approaches

Documents the architectural patterns, design patterns, coding paradigms, and other technical approaches adopted within the component.

Each documented approach should include:

- **Name:** Name of the pattern, paradigm, or approach.
- **Description:** Brief explanation of the approach.
- **Application:** How it is applied within the component.

Rules:

- Only document approaches that have been discussed and approved by the user.
- If no approach has been specified, AI may recommend suitable patterns, paradigms, or approaches for consideration.
- AI must explain each recommendation and its relevance to the component.
- The user must explicitly decide whether to adopt or reject a recommendation.
- AI must not independently introduce or declare an approach as an established architectural decision.
- Do not force the adoption of recognized patterns when they are unnecessary.

### 3.6. Systems

Lists the systems within the component and provides a brief description of each system's responsibility.

Use a table:

| System      | Description                              | Specification                |
| ----------- | ---------------------------------------- | ---------------------------- |
| System Name | Brief description of its responsibility. | [System Specification](link) |

Rules:

- Include only systems belonging to the component.
- Keep descriptions brief.
- Link to their respective System Specification documents when available.
- Detailed technical specifications must be documented separately.

### 3.7. File Structure

Describes the component's directory and file organization.

Include a directory tree with brief descriptions of important directories and files.

Example:

```text
component/
├── system-a/
│   └── Description of the system
├── system-b/
│   └── Description of the system
└── README.md
```

Rules:

- Reflect the actual or approved directory structure.
- Do not invent directories or files.
- Keep descriptions brief.
- Update the structure when the component's organization changes.

### 3.8. Deployment (Optional)

Describes how the component is packaged, deployed, distributed, or executed within the application or its target environment.

Depending on the component, this section may cover:

- Deployment method.
- Packaging and distribution.
- Runtime environment.
- Deployment dependencies.
- Configuration requirements.
- Integration with other deployed components.
- Versioning and release considerations.

Rules:

- Include this section only when deployment information is relevant to the component.
- Document only component-specific deployment details.
- Do not duplicate repository-wide deployment or release documentation.
- Link to related deployment specifications or decision records when available.
- AI may recommend deployment approaches, but the user must approve them before they are documented as adopted decisions.

### 3.9. References

Lists related documentation and external resources relevant to the component.

References may include:

- High-Level Architecture.
- Architecture Decision Records (ADR).
- Architecture Decision Logs (ADL).
- System Specifications.
- System-specific decision records.
- Deployment documentation.
- External technical documentation.

Use descriptive links instead of raw URLs.

## 4. General Guidelines

- Follow the defined section order.
- Keep descriptions concise and technical.
- Avoid duplicating information already documented elsewhere.
- Link to detailed documentation instead of reproducing its contents.
- Use Mermaid diagrams only when they help explain the component's technical organization.
- Maintain consistency with the project's documentation standards.
- Clearly distinguish approved decisions from AI recommendations and proposed approaches.
- Do not assume missing technical decisions. Ask the user or present recommendations for approval.

## 5. File Naming and Pathing Rules

### 5.1. File Path Convention

All Technical Specification documents must be located at:

```
<component>/docs/technical-specification.md
```

Where `<component>` is the name of the component directory (e.g., `database`, `resume-generation`, etc.).

### 5.2. Document Name

The filename must be exactly:

- `technical-specification.md`

No variations, prefixes, or suffixes are allowed.

### 5.3. One Specification Per Component

Each component must have exactly one Technical Specification document.

Rules:

- Do not create multiple technical specification documents for a single component.
- If updating an existing specification, modify the existing file rather than creating a new one.
- When refactoring or restructuring a component, update the path accordingly while maintaining the naming convention.

## 6. Component Specification Path Rules

### 6.1. Required Path Format

All Technical Specification documents must follow this exact path format:

```
<component>/docs/technical-specification.md
```

Where `<component>` is the name of the component directory (e.g., `database`, `resume-generation`, etc.).

### 6.2. Required Document Name

The filename must be exactly:

- `technical-specification.md`

No variations, prefixes, or suffixes are allowed.

### 6.3. Single Specification Per Component

Each component must have exactly one Technical Specification document.

Rules:

- Do not create multiple technical specification documents for a single component.
- If updating an existing specification, modify the existing file rather than creating a new one.
- When refactoring or restructuring a component, update the path accordingly while maintaining the naming convention.
