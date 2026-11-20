from alembic import context

from database.adapters.sqlite.config import SqliteConfig
from database.adapters.sqlite.engine import create_sqlite_engine
from database.adapters.sqlite.llm_log.models import LLMLog
from database.adapters.sqlite.processing_log.models import (
    ResumeProcessingRun,
    ResumeProcessingStep,
)
from database.adapters.sqlite.resume.models.base import Base
from database.adapters.sqlite.resume.models.resume import Resume
from database.adapters.sqlite.resume.models.resume_certification import ResumeCertification
from database.adapters.sqlite.resume.models.resume_education import ResumeEducation
from database.adapters.sqlite.resume.models.resume_experience import ResumeExperience
from database.adapters.sqlite.resume.models.resume_skill import ResumeSkill

config = context.config
_ = (
    LLMLog,
    Resume,
    ResumeCertification,
    ResumeEducation,
    ResumeExperience,
    ResumeProcessingRun,
    ResumeProcessingStep,
    ResumeSkill,
)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    database_url = config.get_main_option("sqlalchemy.url")
    if not database_url:
        raise RuntimeError("sqlalchemy.url must be configured")

    engine = create_sqlite_engine(SqliteConfig(database_url))
    try:
        with engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()
    finally:
        engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
