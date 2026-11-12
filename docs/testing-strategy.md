# Testing Strategy

## 1. Purpose

Define the testing approach for CVBrewery to ensure application behavior meets its requirements and architectural responsibilities.

## 2. Testing Approach

CVBrewery uses a **layered, behavior-oriented testing strategy**.

Tests are organized around the application's architecture:

- **Feature:** Tests whether the feature achieves its intended objective.
- **System:** Tests whether the system fulfills its technical responsibilities.
- **Process:** Tests whether an individual process follows its expected behavior and rules.
- **Module:** Tested independently only when its complexity or behavior justifies it.

## 3. Testing Levels

| Level   | Test Type              | Testing Scope                                                       |
| ------- | ---------------------- | ------------------------------------------------------------------- |
| Feature | Acceptance / E2E       | Connected systems working together to achieve the feature objective |
| System  | Integration / Behavior | System responsibilities and interactions                            |
| Process | Behavior               | Individual process workflows, rules, and expected outcomes          |
| Module  | Optional Unit          | Isolated logic when independently testing it provides value         |

## 4. Testing Rules

1. Tests must verify observable behavior, not implementation details.
2. Every feature must have tests covering its intended objective.
3. Every system should have tests covering its technical responsibilities.
4. Processes should be tested independently when they contain meaningful behavior or rules.
5. Modules do not require tests by default.
6. Avoid duplicating test scenarios across testing levels. Each level must verify its own scope.
7. Prefer real internal components over mocks.
8. Use test doubles for external dependencies when necessary.
9. Use temporary resources for isolated filesystem and database testing, and use the managed `tests/data/` or `tests/e2e/data/` environments for scenarios that intentionally persist between test runs.
10. Maintain a small set of full-application end-to-end tests through the CLI.

## 5. Test Organization

All tests must reside in the repository-level `tests/` directory.

```text
tests/
├── conftest.py
├── data/
├── fixtures/
├── features/
├── systems/
│   └── <system-name>/
│       └── processes/
└── e2e/
    └── data/
```

- `features/`: Feature acceptance tests.
- `systems/`: System integration and behavior tests.
- `processes/`: Individual process behavior tests.
- `e2e/`: Full-application CLI tests.
- `fixtures/`: Shared test data and resources.
- `data/`: Generated test environment data that is reset at the start of every test session.
- `e2e/data/`: Generated end-to-end test environment data that is reset at the start of every test session.

Full test runs order items as follows:

1. Tests marked `application_startup`.
2. Non-end-to-end tests marked `requires_empty_data`.
3. All other non-end-to-end tests.
4. End-to-end tests marked `requires_empty_data`.
5. All other end-to-end tests.

End-to-end tests always run last. Tests marked `requires_empty_data` run before tests that insert test data within their test group.

## 6. Test Scenario Format

Use the **Given–When–Then** pattern to describe test scenarios.

- **Given:** Initial conditions and prerequisites.
- **When:** The action being performed.
- **Then:** Expected behavior and outcomes.

## 7. Testing Principles

- Prioritize important requirements and failure scenarios.
- Avoid unnecessary unit tests and excessive mocking.
- Do not enforce arbitrary code coverage targets.
- Keep tests simple, independent, and maintainable.
- Test according to responsibility and scope, not implementation structure.

## 8. Testing Documentation

The testing component does not have separate documentation. The tests themselves are the documentation for the testing component.

## 9. Test Data Lifecycle

- Managed test data roots are `tests/data/` and `tests/e2e/data/`.
- Both test data layouts mirror the development startup layout: `cvbrewer.db`, `local/resumes/`, and `local/generated/`.
- `tests/data/` and `tests/e2e/data/` are ignored by version control.
- At the start of every test execution session, both test data roots are deleted and recreated as empty folders. Collection-only runs do not reset them.
- Application startup tests are marked `application_startup` and run before all other tests.
- The successful application startup test creates the test data structure under `tests/data/`.
- End-to-end tests initialize and use the test data structure under `tests/e2e/data/`.
- Test data is retained after the test session ends.

## 10. Test Execution Scripts

- `scripts/test-features.sh` runs feature tests.
- `scripts/test-processes.sh` runs process tests.
- `scripts/test-systems.sh` runs system tests.
- `scripts/test-e2e.sh` runs end-to-end tests.
- `scripts/test-all.sh` runs each test level in a separate session, with end-to-end tests last.
- Each script forwards additional arguments to pytest.
- `scripts/test-all.sh` continues through all levels, treats pytest exit code 5 as no collected tests, and returns a nonzero exit code if any level fails.
