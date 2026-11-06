import database


def test_database_package_is_importable() -> None:
    assert database.__name__ == "database"
