from datetime import datetime
from typing import Any

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, sessionmaker

from core.services.processing_log import (
    ProcessingError,
    ProcessingLogRepository,
    ProcessingPerformance,
    ProcessingRunRecord,
    ProcessingStepInput,
    ProcessingStepOutput,
    ProcessingStepRecord,
    ProcessingSummary,
)
from database.adapters.sqlite.engine import session_scope
from database.adapters.sqlite.processing_log.models import (
    ResumeProcessingRun,
    ResumeProcessingStep,
)


def _datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value))


def _optional_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    return _datetime(value)


def _performance(value: Any) -> ProcessingPerformance:
    data = value if isinstance(value, dict) else {}
    return ProcessingPerformance(
        duration_ms=data.get("duration_ms"),
        start_memory_mb=data.get("start_memory_mb"),
        peak_memory_mb=data.get("peak_memory_mb"),
        end_memory_mb=data.get("end_memory_mb"),
        memory_delta_mb=data.get("memory_delta_mb"),
        cpu_avg_percent=data.get("cpu_avg_percent"),
        cpu_peak_percent=data.get("cpu_peak_percent"),
        sample_count=data.get("sample_count", 0),
    )


def _summary(value: Any) -> ProcessingSummary:
    data = value if isinstance(value, dict) else {}
    return ProcessingSummary(
        total_steps=data.get("total_steps", 0),
        completed_steps=data.get("completed_steps", 0),
        failed_steps=data.get("failed_steps", 0),
        skipped_steps=data.get("skipped_steps", 0),
    )


def _error(value: Any) -> ProcessingError | None:
    if not isinstance(value, dict):
        return None
    return ProcessingError(
        code=str(value.get("code", "")),
        type=str(value.get("type", "")),
        message=str(value.get("message", "")),
        details=value.get("details") or {},
        raw=value.get("raw") or {},
        occurred_at=(
            _datetime(value["occurred_at"])
            if value.get("occurred_at") is not None
            else datetime.now()
        ),
    )


def _step_input(value: Any, step_name: str) -> ProcessingStepInput:
    data = value if isinstance(value, dict) else {}
    return ProcessingStepInput(
        type=str(data.get("type", step_name)),
        source_step_id=data.get("source_step_id"),
        size_bytes=data.get("size_bytes"),
        hash=data.get("hash"),
        metadata=data.get("metadata") or {},
        snapshot=data.get("snapshot"),
    )


def _step_output(value: Any, step_name: str) -> ProcessingStepOutput:
    data = value if isinstance(value, dict) else {}
    return ProcessingStepOutput(
        type=str(data.get("type", step_name)),
        size_bytes=data.get("size_bytes"),
        hash=data.get("hash"),
        metadata=data.get("metadata") or {},
        snapshot=data.get("snapshot"),
    )


def _run_to_model(record: ProcessingRunRecord) -> ResumeProcessingRun:
    values = record.as_dict()
    values["started_at"] = _datetime(values["started_at"])
    values["completed_at"] = _optional_datetime(values["completed_at"])
    return ResumeProcessingRun(**values)


def _run_from_model(model: ResumeProcessingRun) -> ProcessingRunRecord:
    return ProcessingRunRecord(
        run_id=model.run_id,
        process_name=model.process_name,
        process_version=model.process_version,
        status=model.status,
        result=model.result,
        resume_id=model.resume_id,
        matched_resume_id=model.matched_resume_id,
        started_at=model.started_at,
        completed_at=model.completed_at,
        duration_ms=model.duration_ms,
        summary=_summary(model.summary),
        performance=_performance(model.performance),
        error=_error(model.error),
    )


def _step_to_model(record: ProcessingStepRecord) -> ResumeProcessingStep:
    values = record.as_dict()
    values["started_at"] = _datetime(values["started_at"])
    values["completed_at"] = _optional_datetime(values["completed_at"])
    values["metadata_json"] = values.pop("metadata")
    return ResumeProcessingStep(**values)


def _step_from_model(model: ResumeProcessingStep) -> ProcessingStepRecord:
    return ProcessingStepRecord(
        step_id=model.step_id,
        run_id=model.run_id,
        step_name=model.step_name,
        step_order=model.step_order,
        attempt_number=model.attempt_number,
        status=model.status,
        started_at=model.started_at,
        completed_at=model.completed_at,
        duration_ms=model.duration_ms,
        input=_step_input(model.input, model.step_name),
        output=_step_output(model.output, model.step_name),
        performance=_performance(model.performance),
        error=_error(model.error),
        metadata=model.metadata_json or {},
    )


class SqliteProcessingLogRepository(ProcessingLogRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def create_run(self, record: ProcessingRunRecord) -> None:
        with session_scope(self._session_factory) as session:
            session.merge(_run_to_model(record))

    def finalize_run(self, record: ProcessingRunRecord) -> None:
        with session_scope(self._session_factory) as session:
            session.merge(_run_to_model(record))

    def create_step(self, record: ProcessingStepRecord) -> None:
        with session_scope(self._session_factory) as session:
            session.merge(_step_to_model(record))

    def finalize_step(self, record: ProcessingStepRecord) -> None:
        with session_scope(self._session_factory) as session:
            session.merge(_step_to_model(record))

    def get_run(self, run_id: str) -> ProcessingRunRecord | None:
        with session_scope(self._session_factory) as session:
            model = session.get(ResumeProcessingRun, run_id)
            return _run_from_model(model) if model is not None else None

    def list_runs(self) -> list[ProcessingRunRecord]:
        with session_scope(self._session_factory) as session:
            statement = select(ResumeProcessingRun).order_by(
                ResumeProcessingRun.started_at
            )
            return [
                _run_from_model(model) for model in session.scalars(statement).all()
            ]

    def list_recent_runs(self, limit: int) -> list[ProcessingRunRecord]:
        with session_scope(self._session_factory) as session:
            statement = (
                select(ResumeProcessingRun)
                .order_by(
                    ResumeProcessingRun.started_at.desc(),
                    ResumeProcessingRun.run_id.desc(),
                )
                .limit(limit)
            )
            return [
                _run_from_model(model) for model in session.scalars(statement).all()
            ]

    def list_error_runs(self, limit: int) -> list[ProcessingRunRecord]:
        with session_scope(self._session_factory) as session:
            statement = (
                select(ResumeProcessingRun)
                .where(
                    or_(
                        ResumeProcessingRun.status.in_(
                            ("FAILED", "VALIDATION_FAILED", "PARTIAL_SUCCESS")
                        ),
                        and_(
                            ResumeProcessingRun.error.is_not(None),
                            ResumeProcessingRun.error != "null",
                        ),
                    )
                )
                .order_by(
                    ResumeProcessingRun.started_at.desc(),
                    ResumeProcessingRun.run_id.desc(),
                )
                .limit(limit)
            )
            return [
                _run_from_model(model) for model in session.scalars(statement).all()
            ]

    def list_steps(
        self,
        run_id: str,
        *,
        limit: int | None = None,
    ) -> list[ProcessingStepRecord]:
        with session_scope(self._session_factory) as session:
            statement = select(ResumeProcessingStep).where(
                ResumeProcessingStep.run_id == run_id
            )
            if limit is None:
                statement = statement.order_by(
                    ResumeProcessingStep.step_order,
                    ResumeProcessingStep.attempt_number,
                )
            else:
                statement = statement.order_by(
                    ResumeProcessingStep.started_at.desc(),
                    ResumeProcessingStep.step_id.desc(),
                ).limit(limit)
            return [
                _step_from_model(model) for model in session.scalars(statement).all()
            ]

    def list_runs_by_resume_id(self, resume_id: str) -> list[ProcessingRunRecord]:
        with session_scope(self._session_factory) as session:
            statement = (
                select(ResumeProcessingRun)
                .where(
                    or_(
                        ResumeProcessingRun.resume_id == resume_id,
                        ResumeProcessingRun.matched_resume_id == resume_id,
                    )
                )
                .order_by(ResumeProcessingRun.started_at)
            )
            return [
                _run_from_model(model) for model in session.scalars(statement).all()
            ]
