from cli.app import app, configure_application
from cli.modules.paths import development_startup_paths
from cli.commands.application_startup import initialize_application
from core.pipeline import ResumeProcessor
from database import create_resume_service, initialize_database
from llm import create_llm_service


def main() -> None:
    paths = initialize_application(development_startup_paths(), initialize_database)
    resume_service = create_resume_service(paths.database)
    llm_service = create_llm_service()
    processor = ResumeProcessor(resume_service, llm_service)
    configure_application(paths, processor)
    app()


if __name__ == "__main__":
    main()
