# Technical System Document Format Rules

## 1. Purpose

This document defines the format and documentation standards for Technical System Documents within CVBrewer.

A Technical System Document describes the technical design, requirements, constraints, and organization of an individual system within a component.

It serves as a technical reference for developers and AI agents during implementation, maintenance, and future development.

A Technical System Document must be supported by an existing high-level System Document and at least one related Architecture Decision Record (ADR).

## 2. Document Structure

### 2.1 Purpose

Describe the technical role of the system and why it exists within the component.

Keep the explanation focused on its technical responsibility.

### 2.2 Objective

Define what the system is expected to accomplish.

Objectives should describe the intended technical outcomes of the system.

### 2.3 Scope

Define the boundaries of the system.

Include:

- Responsibilities within the system.
- What the system handles.
- What the system does not handle.
- Boundaries between this system and other systems or modules.

Avoid duplicating the scope of the high-level System Document.

### 2.4 Rules and Constraints

Document the technical rules and constraints that govern the system.

Include:

- Functional and technical rules.
- Processing requirements.
- Validation requirements.
- Data handling requirements.
- Operational constraints.
- Technical limitations.
- Restrictions on system behavior.

Rules should be clear, specific, and verifiable whenever possible.

### 2.5 Process

List the processes that make up the system.

Each process must link to its corresponding Process Specification Document.

Use the following format:

| Process      | Description                              | Specification                |
| ------------- | ---------------------------------------- | ---------------------------- |
| Process Name | Brief description of its responsibility. | [Process Specification](link) |

Only include processes that belong to the documented system.

### 2.6 Dependencies (Optional)

Document dependencies required by the system.

Dependencies may include:

- Other systems or modules.
- External libraries and frameworks.
- Third-party services.
- External providers.
- Infrastructure or platform requirements.

Briefly explain the purpose of each dependency and link to relevant documentation when available.

Omit this section if the system has no relevant dependencies to document.

### 2.7 Test Cases

Document the test cases required to verify that the system follows its defined rules and constraints.

Each test case should describe:

- Test case ID.
- Test scenario.
- Expected result.
- Related rule or requirement, when applicable.

Test cases should cover normal behavior, boundary conditions, and relevant failure scenarios.

Use a table where appropriate.

### 2.8 Diagrams (Optional)

Include diagrams that help explain the technical structure, interactions, or workflows of the system.

Use Mermaid diagrams where applicable.

Examples:

- Component interaction diagrams.
- Sequence diagrams.
- Process flow diagrams.
- Data flow diagrams.
- System structure diagrams.

Diagrams should explain technical behavior rather than repeat high-level architecture diagrams.

Omit this section when diagrams do not provide additional value.

### 2.9 Architecture Decision Log (ADL)

List the Architecture Decision Records (ADRs) relevant to the technical design of the system.

Each entry must link to its corresponding ADR.

Use the following format:

| ADR               | Decision Summary                   |
| ----------------- | ---------------------------------- |
| [ADR Title](link) | Brief description of the decision. |

The ADL serves as a reference to the decisions that influence the system's technical design.

### 2.10 Data (Optional)

Provide a brief overview of schemas and data models being used by the system.

This section should only be included if the system uses schemas or manages data structures.

Include:

- Schema definitions and their purposes.
- API response/request structures.
- File formats for data exchange.

Omit this section when no schema or structured data is used by the system.

### 2.11 References

List related documentation and external technical references.

Examples:

- High-level System Document.
- Component documentation.
- Process Specification Documents.
- Data model documentation.
- API documentation.
- Official library or framework documentation.

## 3. Documentation Rules

1. A Technical System Document cannot exist independently. It must reference an existing high-level System Document and at least one related ADR.
2. Each document must describe only one system within its parent component.
3. Technical details must remain consistent with approved high-level architecture and ADR decisions.
4. Do not duplicate information from other documentation. Use direct links to relevant documents instead.
5. Keep rules and constraints specific, clear, and verifiable.
6. Process entries must link to their corresponding Process Specification Documents.
7. Test cases must correspond to the documented rules and technical requirements.
8. Optional sections may be omitted when they are not applicable.
9. Update the document when changes affect the system's technical design, responsibilities, rules, or constraints.

## 4. Testing

### 4.1 Test Level

This system should be tested at the **System** level according to the testing strategy.

System-level tests verify:
- System responsibilities and interactions with other components
- Integration between processes within the system
- Technical requirements are met
- System boundaries are respected

### 4.2 Test Scenarios

Document test scenarios using the **Given–When–Then** pattern:

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| System-001 | [Initial conditions] | [Action performed] | [Expected outcome] |

### 4.3 Test Coverage

- Prioritize important requirements and failure scenarios
- Avoid unnecessary unit tests and excessive mocking
- Do not enforce arbitrary code coverage targets
- Keep tests simple, independent, and maintainable
- Test according to responsibility and scope, not implementation structure

### 4.4 Test Organization

Tests for this system should reside in the repository-level `tests/` directory:

```text
tests/
├── systems/
│   └── <system-name>/
│       ├── test_<system>.py
│       └── processes/
│           └── <process-name>/
│               ├── test_<process>.py
│               └── fixtures/
```

### 4.5 Test Dependencies

- Use temporary resources for filesystem and database testing
- Use test doubles for external dependencies when necessary
- Prefer real internal components over mocks where possible

### 4.6 Testing Rules Compliance

This system must follow these testing rules from the testing strategy:

1. Tests must verify observable behavior, not implementation details
2. Every feature must have tests covering its intended objective
3. System responsibilities should be tested independently when they contain meaningful behavior or rules
4. Modules do not require tests by default
5. Avoid duplicating test scenarios across testing levels
6. Prefer real internal components over mocks
7. Use test doubles for external dependencies when necessary
8. Use temporary resources for filesystem and database testing

## 5. References

List related documentation and external technical references.

Examples:

- High-level System Document.
- Component documentation.
- Process Specification Documents.
- Data model documentation.
- API documentation.
- Official library or framework documentation.
