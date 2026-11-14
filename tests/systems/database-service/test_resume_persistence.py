from datetime import date, datetime
from pathlib import Path
from uuid import UUID

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

from database import create_resume_service, initialize_database
from database.adapters.sqlite import (
    AdapterIntegrityError,
    SqliteConfig,
    SqliteResumeRepository,
    create_session_factory,
    create_sqlite_engine,
)
from core.services.resume import (
    Certification,
    Education,
    Experience,
    NewResume,
    ParsedResumeData,
    PersonalInfo,
    ProcessingHistoryEntry,
    ResumeMetadata,
    ResumeService,
    ValidationStatus,
)

_RESUME_TABLES = {
    "resumes",
    "resume_experience",
    "resume_education",
    "resume_certifications",
    "resume_skills",
    "resume_processing_history",
}


def _new_resume(
    *,
    content_fingerprint: str = "fingerprint-1",
    resume_id: str | None = None,
    created_at: datetime | None = None,
) -> NewResume:
    return NewResume(
        resume_id=resume_id,
        created_at=created_at,
        original_file_path=f"/resumes/{content_fingerprint}.pdf",
        metadata=ResumeMetadata(
            file_name=f"{content_fingerprint}.pdf",
            file_size_bytes=2048,
            upload_timestamp=datetime(2026, 1, 1, 9, 0, 0),
            content_fingerprint=content_fingerprint,
        ),
        parsed_data=ParsedResumeData(
            personal_info=PersonalInfo(
                name="Jane Doe",
                email="jane@example.com",
                phone="+1-555-0100",
                address="123 Main Street",
                linkedin_url="https://linkedin.com/in/janedoe",
                github_url="https://github.com/janedoe",
            ),
            summary="Software engineer",
            experience=[
                Experience(
                    company="Acme",
                    position="Senior Engineer",
                    start_date=date(2020, 1, 1),
                    end_date=None,
                    description="Built services",
                ),
                Experience(
                    company="Previous",
                    position="Engineer",
                    start_date=date(2018, 1, 1),
                    end_date=date(2019, 12, 31),
                    description="Maintained applications",
                ),
            ],
            education=[
                Education(
                    institution="University",
                    degree="Bachelor of Science",
                    field_of_study="Computer Science",
                    start_date=date(2014, 9, 1),
                    end_date=date(2018, 5, 31),
                )
            ],
            skills=["Python", "SQL"],
            certifications=[
                Certification(
                    name="Cloud Certification",
                    issuer="Cloud Provider",
                    issue_date=date(2022, 6, 15),
                    expiry_date=None,
                )
            ],
        ),
        validation_status=ValidationStatus(
            file_type_valid=True,
            metadata_extraction_success=True,
            deduplication_result="unique",
            pdf_encryption_check=True,
            pdf_structure_valid=True,
            content_extraction_success=True,
            schema_validation_passed=True,
        ),
        processing_history=[
            ProcessingHistoryEntry(
                step="parse",
                timestamp=datetime(2026, 1, 1, 9, 5, 0),
                status="success",
            )
        ],
    )


def _create_service(database_path: Path) -> tuple[ResumeService, Engine]:
    initialize_database(database_path)
    config = SqliteConfig.from_path(database_path)
    engine = create_sqlite_engine(config)
    session_factory = create_session_factory(engine)
    repository = SqliteResumeRepository(session_factory)
    return ResumeService(repository), engine


def test_migration_creates_resume_schema(tmp_path: Path) -> None:
    database_path = tmp_path / "schema.db"
    _, engine = _create_service(database_path)

    try:
        inspector = inspect(engine)
        assert _RESUME_TABLES.issubset(set(inspector.get_table_names()))

        unique_constraints = inspector.get_unique_constraints("resumes")
        assert any(
            constraint["column_names"] == ["content_fingerprint"]
            for constraint in unique_constraints
        )

        foreign_keys = inspector.get_foreign_keys("resume_experience")
        assert any(
            foreign_key["referred_table"] == "resumes"
            and foreign_key["referred_columns"] == ["resume_id"]
            and foreign_key["options"].get("ondelete") == "CASCADE"
            for foreign_key in foreign_keys
        )
    finally:
        engine.dispose()


def test_create_resume_service_composes_sqlite_adapter(tmp_path: Path) -> None:
    database_path = tmp_path / "composition.db"
    initialize_database(database_path)
    service = create_resume_service(database_path)
    record = _new_resume(
        resume_id="00000000-0000-0000-0000-000000000001",
        created_at=datetime(2026, 1, 1, 10, 0, 0),
    )

    stored_record = service.save_resume(record)

    assert service.get_resume(stored_record.resume_id) == stored_record


def test_save_and_load_round_trip(tmp_path: Path) -> None:
    database_path = tmp_path / "round_trip.db"
    service, engine = _create_service(database_path)
    record = _new_resume(
        resume_id="00000000-0000-0000-0000-000000000001",
        created_at=datetime(2026, 1, 1, 10, 0, 0),
    )

    try:
        stored_record = service.save_resume(record)

        assert service.get_resume(stored_record.resume_id) == stored_record
        assert (
            service.find_resume_by_content_fingerprint("fingerprint-1")
            == stored_record
        )
        assert service.list_resumes() == [stored_record]
    finally:
        engine.dispose()


def test_save_generates_missing_identifier_and_timestamp(tmp_path: Path) -> None:
    database_path = tmp_path / "generated_fields.db"
    service, engine = _create_service(database_path)

    try:
        stored_record = service.save_resume(_new_resume())

        UUID(stored_record.resume_id)
        assert stored_record.created_at is not None
        assert service.get_resume(stored_record.resume_id) == stored_record
    finally:
        engine.dispose()


def test_save_rejects_duplicate_content_fingerprint(tmp_path: Path) -> None:
    database_path = tmp_path / "duplicate.db"
    service, engine = _create_service(database_path)

    try:
        service.save_resume(
            _new_resume(
                resume_id="00000000-0000-0000-0000-000000000001",
                created_at=datetime(2026, 1, 1, 10, 0, 0),
            )
        )

        with pytest.raises(AdapterIntegrityError):
            service.save_resume(
                _new_resume(
                    resume_id="00000000-0000-0000-0000-000000000002",
                    created_at=datetime(2026, 1, 2, 10, 0, 0),
                )
            )

        assert len(service.list_resumes()) == 1
    finally:
        engine.dispose()


def test_missing_lookups_return_none(tmp_path: Path) -> None:
    database_path = tmp_path / "missing.db"
    service, engine = _create_service(database_path)

    try:
        assert service.get_resume("missing") is None
        assert service.find_resume_by_content_fingerprint("missing") is None
    finally:
        engine.dispose()


def test_list_resumes_returns_all_records(tmp_path: Path) -> None:
    database_path = tmp_path / "list.db"
    service, engine = _create_service(database_path)

    try:
        first = service.save_resume(
            _new_resume(
                content_fingerprint="fingerprint-1",
                resume_id="00000000-0000-0000-0000-000000000001",
                created_at=datetime(2026, 1, 1, 10, 0, 0),
            )
        )
        second = service.save_resume(
            _new_resume(
                content_fingerprint="fingerprint-2",
                resume_id="00000000-0000-0000-0000-000000000002",
                created_at=datetime(2026, 1, 2, 10, 0, 0),
            )
        )

        assert service.list_resumes() == [first, second]
    finally:
        engine.dispose()


def test_deleting_resume_cascades_child_records(tmp_path: Path) -> None:
    database_path = tmp_path / "cascade.db"
    service, engine = _create_service(database_path)

    try:
        stored_record = service.save_resume(
            _new_resume(
                resume_id="00000000-0000-0000-0000-000000000001",
                created_at=datetime(2026, 1, 1, 10, 0, 0),
            )
        )

        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM resumes WHERE resume_id = :resume_id"),
                {"resume_id": stored_record.resume_id},
            )

        with engine.connect() as connection:
            for table in _RESUME_TABLES - {"resumes"}:
                count = connection.execute(
                    text(f"SELECT COUNT(*) FROM {table}")
                ).scalar_one()
                assert count == 0
            resume_count = connection.execute(
                text("SELECT COUNT(*) FROM resumes")
            ).scalar_one()
            assert resume_count == 0
    finally:
        engine.dispose()
