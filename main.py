from cli.app import app
from cli.modules.paths import development_startup_paths
from cli.processes.application_startup import initialize_application
from database import initialize_database


def main() -> None:
    initialize_application(development_startup_paths(), initialize_database)
    app()


if __name__ == "__main__":
    main()
