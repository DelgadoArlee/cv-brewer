from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Literal, Protocol

from cli.modules.paths import StartupPaths
from core.services.llm.log_models import LLMLogRecord


class LLMLogQuerier(Protocol):
    def list_all(self) -> list[LLMLogRecord]:
        ...


@dataclass(frozen=True, slots=True)
class LoggerCLIDependencies:
    paths: StartupPaths
    llm_log_querier: LLMLogQuerier


LoggerEnvironment = Literal["dev", "e2e", "test"]
LoggerDependenciesFactory = Callable[[], LoggerCLIDependencies]
LoggerSources = Mapping[LoggerEnvironment, LoggerDependenciesFactory]
