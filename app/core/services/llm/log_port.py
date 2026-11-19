from abc import ABC, abstractmethod

from core.services.llm.log_models import LLMLogRecord


class LLMLogRepository(ABC):
    @abstractmethod
    def save(self, record: LLMLogRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[LLMLogRecord]:
        raise NotImplementedError
