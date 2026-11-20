from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol

from cli.modules.paths import StartupPaths
from core.services.llm.log_models import LLMLogRecord
from core.services.processing_log import ProcessingRunRecord, ProcessingStepRecord

MAX_LOG_ROWS = 100
LoggerEnvironment = Literal["dev", "e2e", "test"]
BrowserOpener = Callable[[str], bool]


class LLMLogQuerier(Protocol):
    def list_all(self) -> list[LLMLogRecord]:
        ...

    def list_recent(self, limit: int) -> list[LLMLogRecord]:
        ...

    def list_errors(self, limit: int) -> list[LLMLogRecord]:
        ...


class ProcessingLogQuerier(Protocol):
    def list_recent_runs(self, limit: int) -> list[ProcessingRunRecord]:
        ...

    def list_error_runs(self, limit: int) -> list[ProcessingRunRecord]:
        ...

    def list_steps(
        self,
        run_id: str,
        *,
        limit: int | None = None,
    ) -> list[ProcessingStepRecord]:
        ...


@dataclass(frozen=True, slots=True)
class LoggerCLIDependencies:
    paths: StartupPaths
    llm_log_querier: LLMLogQuerier
    processing_log_querier: ProcessingLogQuerier
    source: LoggerEnvironment
    logs_dir: Path
    open_browser: BrowserOpener


LoggerDependenciesFactory = Callable[[], LoggerCLIDependencies]
LoggerSources = Mapping[LoggerEnvironment, LoggerDependenciesFactory]
