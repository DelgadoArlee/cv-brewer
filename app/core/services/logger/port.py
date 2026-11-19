from abc import ABC, abstractmethod

from core.services.logger.models import LogEntry


class LogSink(ABC):
    @abstractmethod
    def write(self, entry: LogEntry) -> None:
        raise NotImplementedError
