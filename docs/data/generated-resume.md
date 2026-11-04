# Generated Resume Data Model

## 1. Purpose

This document defines the general data model for generated resume output produced by the AI-powered resume generation system. This structured data represents the tailored resume content that matches a target role while respecting the user's original resume information. The distinction between this model and schema definitions will be determined during implementation.

## 2. JSON Model

```json
{
  "personalInfo": {
    "fullName": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-123-4567",
    "address": {
      "street": "123 Main Street",
      "city": "San Francisco",
      "state": "CA",
      "zipCode": "94102",
      "country": "USA"
    },
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe",
    "website": null,
    "summary": "Experienced software engineer with 5+ years in full-stack development"
  },
  "professionalExperience": [
    {
      "id": 1,
      "company": "Tech Corp",
      "position": "Senior Software Engineer",
      "startDate": "2021-03-01",
      "endDate": null,
      "location": {
        "city": "San Francisco",
        "state": "CA",
        "country": "USA"
      },
      "description": "Led development of scalable backend services using microservices architecture",
      "achievements": [
        "Reduced API response time by 40%",
        "Mentored 3 junior developers"
      ],
      "technologies": ["Python", "Java", "AWS", "Docker"]
    },
    {
      "id": 2,
      "company": "Startup Inc",
      "position": "Software Developer",
      "startDate": "2018-06-01",
      "endDate": "2021-02-28",
      "location": {
        "city": "Austin",
        "state": "TX",
        "country": "USA"
      },
      "description": "Developed and maintained web applications using React and Node.js",
      "achievements": [
        "Launched 3 major product features",
        "Improved user engagement by 25%"
      ],
      "technologies": ["React", "Node.js", "MongoDB", "PostgreSQL"]
    }
  ],
  "education": [
    {
      "id": 1,
      "institution": "University of Technology",
      "degree": "Bachelor of Science in Computer Science",
      "fieldOfStudy": "Computer Science",
      "startDate": "2014-09-01",
      "endDate": "2018-05-31",
      "gpa": "3.8",
      "honors": ["Dean's List", "Graduation with Honors"]
    }
  ],
  "skills": [
    {
      "id": 1,
      "category": "Programming Languages",
      "items": ["Python", "Java", "JavaScript", "TypeScript"]
    },
    {
      "id": 2,
      "category": "Frameworks & Libraries",
      "items": ["React", "Node.js", "Django", "Spring Boot"]
    },
    {
      "id": 3,
      "category": "Tools & Platforms",
      "items": ["AWS", "Docker", "Kubernetes", "Git"]
    }
  ],
  "certifications": [
    {
      "id": 1,
      "name": "AWS Certified Solutions Architect",
      "issuer": "Amazon Web Services",
      "issueDate": "2022-06-15",
      "expiryDate": null
    }
  ],
  "projects": [
    {
      "id": 1,
      "name": "E-commerce Platform",
      "description": "Built a full-stack e-commerce platform with payment integration",
      "technologies": ["React", "Node.js", "MongoDB", "Stripe"],
      "url": "https://github.com/johndoe/ecommerce-platform"
    }
  ],
  "languages": [
    {
      "id": 1,
      "language": "English",
      "proficiency": "Native"
    },
    {
      "id": 2,
      "language": "Spanish",
      "proficiency": "Conversational"
    }
  ],
  "references": null,
  "templateId": "modern-professional",
  "generatedDate": "2024-01-15T10:30:00Z"
}
```

## 3. Data Fields

### Root Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| personalInfo | object | Yes | No | Personal information and contact details | See nested object table below |
| professionalExperience | array | Yes | No | Work history with positions held | See nested object table below |
| education | array | No | Yes | Educational background and degrees | See nested object table below |
| skills | array | No | Yes | Technical and soft skills categorized by type | See nested object table below |
| certifications | array | No | Yes | Professional certifications and credentials | See nested object table below |
| projects | array | No | Yes | Personal or professional projects | See nested object table below |
| languages | array | No | Yes | Languages spoken and proficiency levels | See nested object table below |
| references | string | No | Yes | References section (text or null) | - |
| templateId | string | Yes | No | ID of the resume template used for rendering | Enum: modern-professional, classic-simple, creative-bold |
| generatedDate | string | Yes | No | Timestamp when the resume was generated | ISO 8601 format: YYYY-MM-DDTHH:mm:ssZ |

### Personal Info Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| fullName | string | Yes | No | Full legal name of the candidate | Minimum 2 characters, maximum 100 characters |
| email | string | Yes | No | Email address for contact | Valid email format |
| phone | string | No | Yes | Phone number for contact | E.164 format or null |
| address | object | No | Yes | Physical address (optional) | See nested object table below |
| linkedin | string | No | Yes | LinkedIn profile URL | Valid URL or null |
| github | string | No | Yes | GitHub profile URL | Valid URL or null |
| website | string | No | Yes | Personal website or portfolio URL | Valid URL or null |
| summary | string | No | Yes | Professional summary or objective | Minimum 20 characters, maximum 500 characters |

### Address Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| street | string | No | Yes | Street address | Minimum 2 characters, maximum 100 characters |
| city | string | No | Yes | City name | Minimum 2 characters, maximum 50 characters |
| state | string | No | Yes | State or province | Minimum 2 characters, maximum 50 characters |
| zipCode | string | No | Yes | Postal/ZIP code | - |
| country | string | No | Yes | Country name or code | ISO 3166-1 alpha-2 or full name |

### Professional Experience Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| id | integer | Yes | No | Unique identifier for the experience entry | Sequential integer starting from 1 |
| company | string | Yes | No | Company name where position was held | Minimum 2 characters, maximum 100 characters |
| position | string | Yes | No | Job title or position held | Minimum 2 characters, maximum 100 characters |
| startDate | string | Yes | No | Start date of employment | ISO 8601 format: YYYY-MM-DD |
| endDate | string | No | Yes | End date of employment (null if current) | ISO 8601 format: YYYY-MM-DD or null |
| location | object | No | Yes | Location of the position | See nested object table below |
| description | string | Yes | No | Brief description of role and responsibilities | Minimum 20 characters, maximum 500 characters |
| achievements | array | No | Yes | List of key achievements or accomplishments | See nested object table below |
| technologies | array | No | Yes | Technologies and tools used in the role | - |

### Education Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| id | integer | Yes | No | Unique identifier for the education entry | Sequential integer starting from 1 |
| institution | string | Yes | No | Name of educational institution | Minimum 2 characters, maximum 100 characters |
| degree | string | Yes | No | Degree earned (e.g., Bachelor's, Master's) | - |
| fieldOfStudy | string | Yes | No | Field or major of study | Minimum 2 characters, maximum 100 characters |
| startDate | string | Yes | No | Start date of studies | ISO 8601 format: YYYY-MM-DD |
| endDate | string | Yes | No | End date of studies (null if ongoing) | ISO 8601 format: YYYY-MM-DD or null |
| gpa | string | No | Yes | Grade point average (optional) | - |
| honors | array | No | Yes | Honors and awards received | See nested object table below |

### Skills Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| id | integer | Yes | No | Unique identifier for the skills category | Sequential integer starting from 1 |
| category | string | Yes | No | Category of skills (e.g., Programming Languages) | - |
| items | array | Yes | No | List of skills within the category | - |

### Certification Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| id | integer | Yes | No | Unique identifier for the certification | Sequential integer starting from 1 |
| name | string | Yes | No | Name of the certification | Minimum 2 characters, maximum 100 characters |
| issuer | string | Yes | No | Organization that issued the certification | Minimum 2 characters, maximum 100 characters |
| issueDate | string | Yes | No | Date certification was issued | ISO 8601 format: YYYY-MM-DD |
| expiryDate | string | No | Yes | Expiration date of certification (if applicable) | ISO 8601 format: YYYY-MM-DD or null |

### Project Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| id | integer | Yes | No | Unique identifier for the project | Sequential integer starting from 1 |
| name | string | Yes | No | Project name | Minimum 2 characters, maximum 100 characters |
| description | string | Yes | No | Brief description of the project | Minimum 20 characters, maximum 500 characters |
| technologies | array | No | Yes | Technologies used in the project | - |
| url | string | No | Yes | Link to project repository or website | Valid URL or null |

### Language Object Fields

| Name | Type | Required | Nullable | Description | Constraints |
|------|------|----------|----------|-------------|-------------|
| id | integer | Yes | No | Unique identifier for the language entry | Sequential integer starting from 1 |
| language | string | Yes | No | Language name | Minimum 2 characters, maximum 50 characters |
| proficiency | string | Yes | No | Proficiency level (e.g., Native, Fluent, Conversational) | Enum: Native, Fluent, Intermediate, Basic |

## 4. Validation

- **personalInfo**: Must contain fullName and email; other fields are optional
- **professionalExperience**: Array must contain at least one experience entry with company, position, startDate, and description
- **education**: Optional array; if present, each entry must have institution, degree, fieldOfStudy, startDate, and endDate
- **skills**: Optional array; if present, each category must have items populated
- **certifications**: Optional array; if present, each certification must have name and issuer
- **projects**: Optional array; if present, each project must have name and description
- **languages**: Optional array; if present, each language entry must have language and proficiency
- **references**: Optional string or null
- **templateId**: Must be one of the allowed template IDs
- **generatedDate**: Must be a valid ISO 8601 timestamp

## 5. References

- [Data Model Format Rules](../rules/format/data-model-rules.md)
- [Resume Generation Feature Overview](docs/system/resume-generation/overview.md)
