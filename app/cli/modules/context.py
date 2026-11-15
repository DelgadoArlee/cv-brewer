from dataclasses import dataclass
from typing import Protocol

from cli.modules.paths import StartupPaths
from core.pipeline import ResumeProcessor
from core.services.resume import ResumeRecord


class ResumeLister(Protocol):
    def list_resumes(self) -> list[ResumeRecord]:
        ...


class ResumeDeleter(Protocol):
    def delete_all_resumes(self) -> int:
        ...


@dataclass(frozen=True, slots=True)
class CLIDependencies:
    paths: StartupPaths
    resume_processor: ResumeProcessor
    resume_lister: ResumeLister
    resume_deleter: ResumeDeleter
