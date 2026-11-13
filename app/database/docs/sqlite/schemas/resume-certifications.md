# Resume Certifications Table Schema

## 1. Database Object Identification

- **Name:** `resume_certifications`
- **Type:** Table

## 2. Purpose

Stores ordered certification entries belonging to a stored resume.

## 3. Data Definition

| Name | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | INTEGER | Primary Key, Auto Increment, Not Null | Surrogate identifier for the entry. |
| `resume_id` | TEXT | Foreign Key `resumes.resume_id`, Not Null, On Delete Cascade | Parent resume record. |
| `position_order` | INTEGER | Not Null, Unique with `resume_id` | Preserves source array order. |
| `name` | TEXT | Not Null | Certification name. |
| `issuer` | TEXT | Not Null | Issuing organization. |
| `issue_date` | DATE | Not Null | Date the certification was issued. |
| `expiry_date` | DATE | Nullable | Expiration date, if applicable. |

Indexes:
- Index on `resume_id`.

## 4. Relationships

- Many `resume_certifications` records belong to one `resumes` record.

## 5. Validation

- `resume_id` must reference an existing resume.
- `(resume_id, position_order)` must be unique.
- Required columns must not be null.

## 6. References

- [SQLite Database Overview](../overview.md)
- [User Resume Data Model](../../../../../docs/data/user-resume.md)
