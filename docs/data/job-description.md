# Job Description Data Model

## 1. Purpose

This document defines the general data model for job description information extracted from user-provided job descriptions using LLM-based parsing. This structured data represents the information needed to tailor resume content to a target role. The distinction between this model and schema definitions will be determined during implementation.

## 2. JSON Model

```json
{
  "jobTitle": "Software Engineer",
  "companyName": "Tech Corp",
  "location": {
    "city": "San Francisco",
    "state": "CA",
    "country": "USA",
    "remote": true
  },
  "employmentType": "Full-time",
  "experienceLevel": "Mid-level",
  "responsibilities": [
    {
      "id": 1,
      "description": "Design and develop scalable backend services"
    }
  ],
  "qualifications": [
    {
      "id": 1,
      "type": "Education",
      "requirement": "Bachelor's degree in Computer Science"
    }
  ],
  "preferredQualifications": [
    {
      "id": 1,
      "type": "Experience",
      "requirement": "Cloud platform experience preferred"
    }
  ],
  "benefits": [
    {
      "id": 1,
      "description": "Competitive salary and equity package"
    }
  ],
  "applicationDeadline": null,
  "sourceUrl": null
}
```

## 3. Data Fields

### Root Object Fields

| Name                    | Type   | Required | Nullable | Description                                | Constraints                   |
| ----------------------- | ------ | -------- | -------- | ------------------------------------------ | ----------------------------- |
| jobTitle                | string | Yes      | No       | The official job title for the position    | -                             |
| companyName             | string | Yes      | No       | The name of the hiring company             | -                             |
| location                | object | Yes      | No       | Geographic location and remote work status | See nested object table below |
| employmentType          | string | Yes      | No       | Type of employment                         | -                             |
| experienceLevel         | string | Yes      | No       | Required experience level                  | -                             |
| responsibilities        | array  | Yes      | No       | List of job responsibilities and duties    | See nested object table below |
| qualifications          | array  | Yes      | No       | Required qualifications for the position   | See nested object table below |
| preferredQualifications | array  | No       | Yes      | Preferred but not required qualifications  | See nested object table below |
| benefits                | array  | No       | Yes      | List of employee benefits offered          | See nested object table below |
| applicationDeadline     | string | No       | Yes      | Application deadline date                  | -                             |
| sourceUrl               | string | No       | Yes      | URL to the original job posting            | -                             |

### Location Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| city | string | Yes | No | City where the position is located | - |
| state | string | No | Yes | State or province (if applicable) | - |
| country | string | Yes | No | Country where the position is located | - |
| remote | boolean | Yes | No | Whether the position is remote or on-site | - |

### Responsibility Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| id | integer | Yes | No | Unique identifier for the responsibility | - |
| description | string | Yes | No | Description of the responsibility or duty | - |

### Qualification Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| id | integer | Yes | No | Unique identifier for the qualification | - |
| type | string | Yes | No | Category of qualification | - |
| requirement | string | Yes | No | Specific requirement or description | - |

### Preferred Qualification Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| id | integer | Yes | No | Unique identifier for the preferred qualification | - |
| type | string | Yes | No | Category of preferred qualification | - |
| requirement | string | Yes | No | Specific preferred qualification description | - |

### Benefit Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| id | integer | Yes | No | Unique identifier for the benefit | - |
| description | string | Yes | No | Description of the employee benefit | - |

## 4. Validation

- Job title and company name must be present and non-empty
- Location information is required with city and country at minimum
- Employment type and experience level must be specified
- Responsibilities and qualifications arrays must contain at least one item
- Preferred qualifications and benefits are optional
- Application deadline and source URL are optional fields

## 5. References

- [Data Model Format Rules](../rules/format/data-model-rules.md)
