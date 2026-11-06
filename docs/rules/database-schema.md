# Database Schema Documentation Rules

## Purpose

- Documents the database-specific schema of data persisted in a database.
- Applies only to data that is stored in a database.
- The schema format depends on the database type and implementation.
- Documents must be stored at:
  `database/docs/<database-service-name>/schemas/<schema-name>.md`

## Documentation Structure

### Required Sections

1. **Database Object Identification**
   - Identify the database object being documented (e.g., table, model, collection, or document).
   - Specify its name and object type.

2. **Purpose**
   - Describe the purpose of the database object.

3. **Data Definition**
   - Define the data structure using the following fields:
     - **Name:** Field, column, or property name.
     - **Type:** Database-specific data type.
     - **Constraints:** Database-enforced restrictions or rules applied to the field, such as:
       - Primary Key
       - Foreign Key
       - Unique
       - Not Null
       - Default Value
       - Check Constraint
       - Index (where applicable)
     - **Description:** Explain the field's purpose.

### Optional Sections

4. **Relationships**
   - Document related database objects and their cardinality, where applicable.

5. **Validation**
   - Document additional database-level validation rules not covered by field constraints, where applicable.

6. **References**
   - Include relevant documentation, specifications, or related resources.
