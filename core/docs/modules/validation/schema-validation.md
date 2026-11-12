# Resume Processing Schema Validation Module Technical Specification

## 1. Purpose

Loads the Resume JSON Schema, validates structured resume payloads, and converts valid payloads into Database Service resume records. The implementation is located at `core/src/core/validation/schema_validation.py`; Pydantic validation models are defined in `core/src/core/validation/models/resume.py`.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `load_resume_schema()` | Function | Loads and caches the packaged Resume JSON Schema. | None. | `dict[str, Any]` – Resume JSON Schema. |
| `validate_resume_payload()` | Function | Validates a payload with JSON Schema and Pydantic, then converts it to Database Service records. | `payload: dict[str, Any]` – Merged resume payload. | `ParsedResumeData` – Validated parsed resume data; raises `ResumeSchemaError` when invalid. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `jsonschema` | External library | Validates payloads against the Resume JSON Schema. |
| `pydantic` | External library | Provides runtime validation and typed resume models. |
| Python `importlib.resources` | Standard library | Loads the packaged schema file. |
| Database Service resume models | Internal dependency | Provides parsed resume records. |
| Validation models | Internal module | Provides Pydantic models for parsed resume payloads. |
| Resume processing errors | Internal module | Provides `ResumeSchemaError`. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/12/2026 | Derive the Resume JSON Schema from the user resume data model and validate with `jsonschema` and Pydantic. | `load_resume_schema()`, `validate_resume_payload()` | [Resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md) |

## 5. References

- [Resume Processing Technical System Specification](../../systems/resume-processing/overview.md)
- [Validation Models Module](validation-models.md)
- [Schema Validation Process](../../../../docs/system/resume-processing/processes/7-schema-validation.md)
- [User Resume Data Model](../../../../docs/data/user-resume.md)
- [Use JSON Schema and Pydantic for data validation](../../../../docs/adr/Architecture/2026-11-04/schema-validation.md)
