# Data Schema Documentation Rules

**File location:** `<component>/docs/schema/<schema-name>.md`

## 1. Purpose

- Describe the structure, fields, and constraints of a data object used within a component.
- This document is intended for data that is not persisted in a database.
- Database-persisted data must use the database schema documentation standard instead.

## 2. Object Type

- Identify the type of data object.
- Supported types include:
  - **DTO:** Data Transfer Object used to transfer data between components or layers.
  - **Validation:** Schema used to validate data structure and values.
  - **Cache:** Data structure used to temporarily store in-memory data.
- Specify the object type clearly. Other types may be introduced when necessary.

## 3. JSON Model

- Provide a JSON representation of the data structure.
- Use representative values to demonstrate the expected structure.
- Use `null` for nullable fields and appropriate values for other field types.
- Include nested objects and arrays where applicable.

## 4. Data Table

Document each field using the following columns:

| Name          | Type           | Constraints         | Description             |
| ------------- | -------------- | ------------------- | ----------------------- |
| `id`          | string         | Required, non-empty | Unique identifier.      |
| `name`        | string         | Required, non-empty | Name of the object.     |
| `description` | string or null | Optional            | Additional information. |

- **Name:** Field name.
- **Type:** Expected data type.
- **Constraints:** Required, optional, nullable, allowed values, formats, or other applicable restrictions.
- **Description:** Brief explanation of the field's purpose.

## 5. References

- List relevant documentation, specifications, or related schemas.
- Use relative Markdown links when referencing repository documents.
- Omit this section when no references are applicable.
