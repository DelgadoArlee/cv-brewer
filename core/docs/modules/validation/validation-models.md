# Resume Processing Validation Models Module Technical Specification

## 1. Purpose

Defines the Pydantic models used to validate parsed resume payloads before conversion to Database Service records. The implementation is located at `core/src/core/validation/models/resume.py`.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `PersonalInfoModel` | Pydantic model | Validates resume contact information. | Parsed personal information fields. | `PersonalInfoModel` instance. |
| `ExperienceModel` | Pydantic model | Validates one work experience entry. | Company, position, dates, and description. | `ExperienceModel` instance. |
| `EducationModel` | Pydantic model | Validates one education entry. | Institution, degree, field of study, and dates. | `EducationModel` instance. |
| `CertificationModel` | Pydantic model | Validates one certification entry. | Name, issuer, issue date, and optional expiry date. | `CertificationModel` instance. |
| `ParsedResumePayloadModel` | Pydantic model | Validates the complete parsed resume payload. | Personal information, summary, experience, education, skills, and certifications. | `ParsedResumePayloadModel` instance. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| Pydantic | External library | Provides validation models and configuration. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/12/2026 | Separate validation models from validation logic and organize Core code by responsibility. | All models | [Organize Core packages by responsibility](../../adr/11-12-26/core-package-structure.md) |

## 5. References

- [Resume Processing Technical System Specification](../../systems/resume-processing/overview.md)
- [Schema Validation Module](schema-validation.md)
- [Use JSON Schema and Pydantic for data validation](../../../../docs/adr/Architecture/2026-11-04/schema-validation.md)
