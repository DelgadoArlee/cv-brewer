from abc import ABC, abstractmethod

from core.services.processing_log.models import (
    ProcessingRunRecord,
    ProcessingStepRecord,
)


class ProcessingLogRepository(ABC):
    @abstractmethod
    def create_run(self, record: ProcessingRunRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    def finalize_run(self, record: ProcessingRunRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_step(self, record: ProcessingStepRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    def finalize_step(self, record: ProcessingStepRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_run(self, run_id: str) -> ProcessingRunRecord | None:
        raise NotImplementedError

    @abstractmethod
    def list_runs(self) -> list[ProcessingRunRecord]:
        raise NotImplementedError

    @abstractmethod
    def list_recent_runs(self, limit: int) -> list[ProcessingRunRecord]:
        raise NotImplementedError

    @abstractmethod
    def list_error_runs(self, limit: int) -> list[ProcessingRunRecord]:
        raise NotImplementedError

    @abstractmethod
    def list_steps(
        self,
        run_id: str,
        *,
        limit: int | None = None,
    ) -> list[ProcessingStepRecord]:
        raise NotImplementedError

    @abstractmethod
    def list_runs_by_resume_id(self, resume_id: str) -> list[ProcessingRunRecord]:
        raise NotImplementedError
