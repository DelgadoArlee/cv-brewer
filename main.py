from cli.app import create_app
from cli.commands.application_startup import initialize_application
from cli.modules.context import CLIDependencies
from cli.modules.paths import StartupPaths, development_startup_paths
from core.pipeline import ResumeProcessor
from database import create_resume_service, initialize_database
from llm import create_llm_service


def build_dependencies(paths: StartupPaths) -> CLIDependencies:
    prepared_paths = initialize_application(paths, initialize_database)
    resume_service = create_resume_service(prepared_paths.database)
    llm_service = create_llm_service()
    processor = ResumeProcessor(resume_service, llm_service)
    return CLIDependencies(prepared_paths, processor, resume_service)


def main() -> None:
    create_app(build_dependencies(development_startup_paths()))()


if __name__ == "__main__":
    main()
