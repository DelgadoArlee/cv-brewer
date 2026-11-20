from cli.app import create_app
from cli.commands.application_startup import initialize_application
from cli.modules.context import CLIDependencies
from cli.modules.paths import StartupPaths, development_startup_paths
from core.pipeline import ResumeProcessor
from core.services.logger import LoggerService
from core.services.llm.logger import LLMLogger
from database import (
    create_llm_log_service,
    create_processing_log_service,
    create_resume_service,
    initialize_database,
)
from llm import create_llm_service


def build_dependencies(paths: StartupPaths) -> CLIDependencies:
    prepared_paths = initialize_application(paths, initialize_database)
    resume_service = create_resume_service(prepared_paths.database)
    llm_log_repository = create_llm_log_service(prepared_paths.database)
    logger_service = LoggerService([llm_log_repository])
    llm_logger = LLMLogger("ollama", logger_service)
    llm_service = create_llm_service(logger=llm_logger)
    processing_log_service = create_processing_log_service(prepared_paths.database)
    processor = ResumeProcessor(resume_service, llm_service, processing_log_service)
    return CLIDependencies(prepared_paths, processor, resume_service, resume_service)


def main() -> None:
    create_app(build_dependencies(development_startup_paths()))()


if __name__ == "__main__":
    main()
