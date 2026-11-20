import logging
from datetime import datetime
from typing import Any
from uuid import uuid4

from core.services.logger.models import utc_now
from core.services.processing_log.models import (
    ProcessingLogStatus,
    ProcessingPerformance,
    ProcessingRunRecord,
    ProcessingStepInput,
    ProcessingStepOutput,
    ProcessingStepRecord,
    ProcessingSummary,
)
from core.services.processing_log.port import ProcessingLogRepository

_LOGGER = logging.getLogger(__name__)


def _report_failure(action: str, exc: Exception) -> None:
    _LOGGER.error("Failed to %s.", action, exc_info=exc)


class ProcessingLogService:
    def __init__(self, repository: ProcessingLogRepository) -> None:
        self._repository = repository

    @staticmethod
    def new_run_id() -> str:
        return str(uuid4())

    @staticmethod
    def new_step_id() -> str:
        return str(uuid4())

    def start_run(
        self,
        *,
        process_name: str,
        process_version: str,
        run_id: str | None = None,
        started_at: datetime | None = None,
    ) -> ProcessingRunRecord:
        record = ProcessingRunRecord(
            run_id=run_id or self.new_run_id(),
            process_name=process_name,
            process_version=process_version,
            status=ProcessingLogStatus.RUNNING,
            result=None,
            resume_id=None,
            matched_resume_id=None,
            started_at=started_at or utc_now(),
            completed_at=None,
            duration_ms=None,
            summary=ProcessingSummary(),
            performance=ProcessingPerformance(),
            error=None,
        )
        try:
            self._repository.create_run(record)
        except Exception as exc:
            _report_failure("create processing run", exc)
        return record

    def finalize_run(self, record: ProcessingRunRecord) -> ProcessingRunRecord:
        try:
            self._repository.finalize_run(record)
        except Exception as exc:
            _report_failure("finalize processing run", exc)
        return record

    def start_step(
        self,
        *,
        run_id: str,
        step_name: str,
        step_order: int,
        attempt_number: int = 1,
        step_id: str | None = None,
        input_data: ProcessingStepInput | None = None,
        output_data: ProcessingStepOutput | None = None,
        metadata: dict[str, Any] | None = None,
        started_at: datetime | None = None,
    ) -> ProcessingStepRecord:
        record = ProcessingStepRecord(
            step_id=step_id or self.new_step_id(),
            run_id=run_id,
            step_name=step_name,
            step_order=step_order,
            attempt_number=attempt_number,
            status=ProcessingLogStatus.RUNNING,
            started_at=started_at or utc_now(),
            completed_at=None,
            duration_ms=None,
            input=input_data or ProcessingStepInput(type=step_name),
            output=output_data or ProcessingStepOutput(type=step_name),
            performance=ProcessingPerformance(),
            error=None,
            metadata=metadata or {},
        )
        try:
            self._repository.create_step(record)
        except Exception as exc:
            _report_failure("create processing step", exc)
        return record

    def finalize_step(self, record: ProcessingStepRecord) -> ProcessingStepRecord:
        try:
            self._repository.finalize_step(record)
        except Exception as exc:
            _report_failure("finalize processing step", exc)
        return record

    def get_run(self, run_id: str) -> ProcessingRunRecord | None:
        try:
            return self._repository.get_run(run_id)
        except Exception as exc:
            _report_failure("get processing run", exc)
            return None

    def list_runs(self) -> list[ProcessingRunRecord]:
        try:
            return self._repository.list_runs()
        except Exception as exc:
            _report_failure("list processing runs", exc)
            return []

    def list_recent_runs(self, limit: int) -> list[ProcessingRunRecord]:
        try:
            return self._repository.list_recent_runs(limit)
        except Exception as exc:
            _report_failure("list recent processing runs", exc)
            return []

    def list_error_runs(self, limit: int) -> list[ProcessingRunRecord]:
        try:
            return self._repository.list_error_runs(limit)
        except Exception as exc:
            _report_failure("list error processing runs", exc)
            return []

    def list_steps(
        self,
        run_id: str,
        *,
        limit: int | None = None,
    ) -> list[ProcessingStepRecord]:
        try:
            return self._repository.list_steps(run_id, limit=limit)
        except Exception as exc:
            _report_failure("list processing steps", exc)
            return []

    def list_runs_by_resume_id(self, resume_id: str) -> list[ProcessingRunRecord]:
        try:
            return self._repository.list_runs_by_resume_id(resume_id)
        except Exception as exc:
            _report_failure("list processing runs by resume identifier", exc)
            return []
