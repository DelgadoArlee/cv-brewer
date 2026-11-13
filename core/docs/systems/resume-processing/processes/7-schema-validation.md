# Schema Validation Technical Process

## 1. Purpose

Define how the Core Processing Engine validates a structured resume payload before storage.

## 2. Objective

- Validate the payload against the Resume JSON Schema.
- Validate and convert the payload into Database Service resume records.
- Reject invalid payloads without storing partial data.

## 3. Scope

### In Scope

- Loading and checking the Resume JSON Schema.
- JSON Schema validation with format checking.
- Pydantic model validation and conversion to resume data records.
- Raising schema errors for invalid payloads.

### Out of Scope

- LLM generation and merging.
- Database persistence.
- Schema authoring and migration.

## 4. Rules & Constraints

- Validate the complete merged payload only.
- Load the schema from `core/src/core/validation/schemas/resume.json`.
- Use JSON Schema Draft 2020-12 validation with format checking.
- Reject payloads that fail JSON Schema validation.
- Reject payloads that fail Pydantic validation.
- Reject an invalid schema as a resume schema error.
- Return Database Service resume records only after all validation succeeds.
- Do not store partial or invalid records.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    Start([Merged payload]) --> Load[Load resume schema]
    Load -->|Invalid schema| SchemaError[Raise schema error]
    Load --> JsonSchema{JSON Schema valid?}
    JsonSchema -->|No| SchemaError
    JsonSchema -->|Yes| Pydantic{Pydantic model valid?}
    Pydantic -->|No| SchemaError
    Pydantic -->|Yes| Convert[Convert to resume records]
    Convert --> Return[Return validated resume data]
````

### Steps

1. Load the cached Resume JSON Schema.
2. Check the schema with the Draft 2020-12 validator.
3. Validate the payload with format checking.
4. Raise a schema error when JSON Schema validation fails.
5. Validate the payload with Pydantic models.
6. Raise a schema error when Pydantic validation fails.
7. Convert the validated payload into Database Service resume records.
8. Return the validated resume data for storage.

## 6. Modules

- `core/src/core/validation/schema_validation.py` — Implements schema loading, validation, and record conversion.
- `core/src/core/validation/models/resume.py` — Defines the Pydantic payload models.
- `core/src/core/validation/schemas/resume.json` — Defines the Resume JSON Schema.
- `core/src/core/pipeline/resume_processing.py` — Invokes schema validation before storage.
- `core/src/core/errors.py` — Defines the resume schema error.

## 7. Data

- [Resume JSON Schema](../../../../src/core/validation/schemas/resume.json) — Defines the parsed resume payload contract.
- [User Resume Data Model](../../../../../docs/data/user-resume.md) — Defines the resume data contract.

## 8. Testing

### 8.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| RP-SCHEMA-001 | A schema-valid resume payload. | Schema validation runs. | Validated resume data is returned. |
| RP-SCHEMA-002 | A payload missing required fields. | Schema validation runs. | A resume schema error is raised. |
| RP-SCHEMA-003 | A payload with invalid field formats. | Schema validation runs. | A resume schema error is raised. |
| RP-SCHEMA-004 | An invalid Resume JSON Schema. | Schema validation runs. | A resume schema error is raised. |

## 9. References

- [Resume Processing Technical Process](resume-processing.md)
- [Resume Processing System Overview](../overview.md)
- [Core Component Technical Specification](../../../technical-specification.md)
- [User Resume Data Model](../../../../../docs/data/user-resume.md)
