# Resume Education Table Schema

## 1. Database Object Identification

- **Name:** `resume_education`
- **Type:** Table

## 2. Purpose

Stores ordered education entries belonging to a stored resume.

## 3. Data Definition

| Name | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | INTEGER | Primary Key, Auto Increment, Not Null | Surrogate identifier for the entry. |
| `resume_id` | TEXT | Foreign Key `resumes.resume_id`, Not Null, On Delete Cascade | Parent resume record. |
| `position_order` | INTEGER | Not Null, Unique with `resume_id` | Preserves source array order. |
| `institution` | TEXT | Not Null | Educational institution name. |
| `degree` | TEXT | Not Null | Degree obtained. |
| `field_of_study` | TEXT | Nullable | Field of study or major. |
| `start_date` | DATE | Not Null | Start date of studies. |
| `end_date` | DATE | Nullable | End date of studies. |

Indexes:
- Index on `resume_id`.

## 4. Relationships

- Many `resume_education` records belong to one `resumes` record.

## 5. Validation

- `resume_id` must reference an existing resume.
- `(resume_id, position_order)` must be unique.
- Required columns must not be null.

## 6. References

- [SQLite Database Overview](../overview.md)
- [User Resume Data Model](../../../../../docs/data/user-resume.md)
