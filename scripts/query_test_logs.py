import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from cli.modules.paths import startup_paths
from database import create_llm_log_service

TEST_DATA_PATH = Path(__file__).resolve().parents[1] / "tests" / "data"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query LLM activity logs from the test database.",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=startup_paths(TEST_DATA_PATH).database,
        help="Path to the test database.",
    )
    return parser.parse_args()


def query_logs(database_path: Path) -> list[dict[str, Any]]:
    if not database_path.is_file():
        raise SystemExit(f"Test database not found: {database_path}")

    repository = create_llm_log_service(database_path)
    return [asdict(record) for record in repository.list_all()]


def main() -> None:
    args = parse_args()
    print(json.dumps(query_logs(args.database), indent=2, default=str))


if __name__ == "__main__":
    main()
