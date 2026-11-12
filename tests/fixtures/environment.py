import shutil
from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parents[1]
TEST_DATA_PATH = TESTS_ROOT / "data"
E2E_TESTS_PATH = TESTS_ROOT / "e2e"
E2E_DATA_PATH = E2E_TESTS_PATH / "data"


def reset_data_directory(data_path: Path) -> None:
    if data_path.exists():
        if data_path.is_dir():
            shutil.rmtree(data_path)
        else:
            data_path.unlink()

    data_path.mkdir(parents=True)
