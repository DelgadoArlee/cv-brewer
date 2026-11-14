from abc import ABC, abstractmethod

from core.services.resume.models import ResumeRecord


class ResumeRepository(ABC):
    @abstractmethod
    def save(self, record: ResumeRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, resume_id: str) -> ResumeRecord | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_content_fingerprint(
        self,
        content_fingerprint: str,
    ) -> ResumeRecord | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[ResumeRecord]:
        raise NotImplementedError
