# Technical Process Documentation

## 1. Purpose

Describe the implementation details of a process and define the rules for documenting its internal workflow.

## 2. Objective

Define what the process must accomplish from a technical perspective.

## 3. Scope

Define the responsibilities and boundaries of the process, including what is and is not handled by it.

## 4. Rules & Constraints

List the implementation rules, conditions, and limitations that the process must follow.

- Define required conditions and validations.
- Specify important processing rules.
- Identify error-handling requirements.
- Avoid documenting implementation details outside the process scope.

## 5. Workflow

### Diagram

Provide a Mermaid diagram illustrating the process flow, including important decisions and processing steps.

- For processes with user-visible interaction, include the UI flow of user actions, prompts or menus, and displayed outcomes in the diagram.
- Keep the UI flow concise.

### Steps

Describe each workflow step in execution order.

- Keep descriptions concise.
- Focus on what each step does.
- Include important conditions and outcomes.

## 6. Modules

List the modules used in the process, reference their actual source files using absolute repository paths, and briefly describe their responsibilities.

- `app/core/modules/parsing.py` — Brief description.

Only include modules directly involved in executing the process.

## 7. Data _(Optional)_

List the schemas used or produced by the process.

- [Schema Name](path/to/schema.md) — Brief description.

Only include this section when the process uses or produces structured data with a documented schema.

## 8. Testing

### 8.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

Process-level tests verify:
- Individual process workflows follow expected behavior and rules
- Each step executes correctly in sequence
- Error handling works as specified
- Boundary conditions are handled properly

### 8.2 Test Scenarios

Document test scenarios using the **Given–When–Then** pattern:

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| Process-001 | [Initial conditions] | [Action performed] | [Expected outcome] |

### 8.3 Test Coverage

- Prioritize important requirements and failure scenarios
- Avoid unnecessary unit tests and excessive mocking
- Do not enforce arbitrary code coverage targets
- Keep tests simple, independent, and maintainable
- Test according to responsibility and scope, not implementation structure

### 8.4 Test Organization

Tests for this process should reside in the repository-level `tests/` directory:

```text
tests/
├── processes/
│   └── <process-name>/
│       ├── test_<process>.py
│       └── fixtures/
```

### 8.5 Test Dependencies

- Use temporary resources for filesystem and database testing
- Use test doubles for external dependencies when necessary
- Prefer real internal components over mocks where possible

### 8.6 Testing Rules Compliance

This process must follow these testing rules from the testing strategy:

1. Tests must verify observable behavior, not implementation details
2. Every feature must have tests covering its intended objective
3. Processes should be tested independently when they contain meaningful behavior or rules
4. Modules do not require tests by default
5. Avoid duplicating test scenarios across testing levels
6. Prefer real internal components over mocks
7. Use test doubles for external dependencies when necessary
8. Use temporary resources for filesystem and database testing

## 9. References

List related documentation, dependencies, and external references.

- [Reference Name](path/to/reference.md)
