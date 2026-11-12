# Resume Skills Table Schema

## 1. Database Object Identification

- **Name:** `resume_skills`
- **Type:** Table

## 2. Purpose

Stores ordered skill entries belonging to a stored resume.

## 3. Data Definition

| Name | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | INTEGER | Primary Key, Auto Increment, Not Null | Surrogate identifier for the skill. |
| `resume_id` | TEXT | Foreign Key `resumes.resume_id`, Not Null, On Delete Cascade | Parent resume record. |
| `position_order` | INTEGER | Not Null, Unique with `resume_id` | Preserves source array order. |
| `skill` | TEXT | Not Null | Skill value. |

Indexes:
- Index on `resume_id`.

## 4. Relationships

- Many `resume_skills` records belong to one `resumes` record.

## 5. Validation

- `resume_id` must reference an existing resume.
- `(resume_id, position_order)` must be unique.
- `skill` must not be null.

## 6. References

- [SQLite Database Overview](../overview.md)
- [User Resume Data Model](../../../../docs/data/user-resume.md)
