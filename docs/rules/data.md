# Data Model Format Rules

## 1. Purpose

This document defines the standard format for documenting data models within CVBrewery. It ensures consistency, clarity, and completeness across all data model documentation.

## 2. Documentation Requirements

Every data model documentation must contain the following sections:

### 2.1 Description

Provides a brief explanation of the data model, including:

- Its purpose.
- What information it represents.
- How it is used within the system.

### 2.2 JSON Model

Provides a JSON representation of the data model.

- Must represent the structure of the data.
    
- Must use descriptive field names.
    
- Must represent nested objects and arrays where applicable.
    
- Must use representative values or clearly indicated data types.
    
- Must not include database-specific structures or syntax.
    

**Example:**

````
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "phoneNumber": null,
  "skills": [
    {
      "name": "Python",
      "category": "Programming"
    }
  ],
  "experience": [
    {
      "company": "ABC Corporation",
      "position": "Software Developer",
      "startDate": "2022-01-01",
      "endDate": null
    }
  ]
}
````

The example illustrates representative values, optional fields using `null`, arrays, and nested objects.

### 2.3 Data Fields

Provides tables describing each field in the data model.

Each table must include:

| Column      | Description                                                                     |
| ----------- | ------------------------------------------------------------------------------- |
| Name        | Name of the field.                                                              |
| Type        | Data type of the field.                                                         |
| Required    | Indicates whether the field is required.                                        |
| Nullable    | Indicates wheter the field can contain null                                     |
| Description | Explains the purpose of the field.                                              |
| Constraints | Defines restrictions such as minimum length, maximum length, or allowed values. |

Additional columns may be included when necessary.

**Nested Object Rules:**

- Each nested object must have its own data-field table.
- Nested object tables must be identified by their parent field name.
- Arrays of objects must follow the same rule.
- The parent table must identify nested objects and arrays by their corresponding type and reference to their own table.
- Nested structures must maintain their hierarchical relationships.

### 2.4 Validation

Defines the validation requirements for the data model and its fields.

- Specify accepted values or formats where applicable.
- Define restrictions or constraints on individual fields.
- Define validation requirements for nested objects and arrays.
- Define any relationships or dependencies between fields.

### 2.5 References

Lists relevant documentation, specifications, or external resources used as references for the data model.

References may include:

- Related data models.
- Internal system documentation.
- External specifications or standards.
- Relevant technical documentation.

## 3. General Formatting Rules

- Use `snake_case` for field names for .
- Use consistent naming conventions across data models.
- Use standard JSON data types when representing data.
- Use `null` to represent fields that may have no value.
- Clearly distinguish between required and optional fields.
- Use consistent date and timestamp formats.
- Keep descriptions concise and specific.
- Avoid database-specific terminology and implementation details unless necessary for describing the data itself.
