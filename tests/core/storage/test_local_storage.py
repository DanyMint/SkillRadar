"""Tests for the LocalStorage implementation."""

import json
from dataclasses import asdict
from pathlib import Path

import pytest

from skillradar.core.fetch.models import RawVacancy
from skillradar.core.normalize.models import NormalizedVacancy
from skillradar.core.storage.local import LocalStorage

TEST_APP_DIR_NAME = ".skillradar_test"


@pytest.fixture
def temp_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> LocalStorage:
    """
    Fixture to create a LocalStorage instance in a temporary directory.

    This fixture mocks the user's home directory (`Path.home`) so that
    the LocalStorage instance reads from and writes to a temporary
    directory created by pytest, preventing tests from affecting the
    real user data.
    """
    # Create a fake home directory
    fake_home = tmp_path / "user"
    fake_home.mkdir()

    # Monkeypatch Path.home() to return our fake home
    monkeypatch.setattr(Path, "home", lambda: fake_home)

    # The LocalStorage will now use ~/.skillradar_test inside the fake home
    # We need to re-import paths after monkeypatching to make it use the mocked home
    from skillradar.core.storage import paths

    monkeypatch.setattr(paths, "APP_DIR", fake_home / TEST_APP_DIR_NAME)
    paths.DATA_DIR = paths.APP_DIR / "data"
    paths.RAW_DIR = paths.DATA_DIR / "raw"
    paths.NORMALIZED_DIR = paths.DATA_DIR / "normalized"

    return LocalStorage()


def test_ensure_dirs_creates_directories(temp_storage: LocalStorage):
    """
    Verify that ensure_dirs creates the raw and normalized data directories.
    """
    # Arrange
    storage = temp_storage

    # We need to access the paths module that was re-imported inside the fixture
    from skillradar.core.storage import paths

    # Act
    storage.ensure_dirs()

    # Assert
    assert paths.RAW_DIR.exists()
    assert paths.RAW_DIR.is_dir()
    assert paths.NORMALIZED_DIR.exists()
    assert paths.NORMALIZED_DIR.is_dir()


def test_save_and_load_raw(temp_storage: LocalStorage):
    """
    Verify that raw data can be saved and loaded correctly.
    """
    # Arrange
    storage = temp_storage
    test_name = "test_raw_data"
    test_data = {"id": "123", "value": "some_data", "nested": {"a": 1}}

    # Act
    storage.save_raw(test_name, test_data)
    loaded_data = storage.load_raw(test_name)

    # Assert
    assert loaded_data == test_data


def test_save_and_load_normalized(temp_storage: LocalStorage):
    """
    Verify that normalized data can be saved and loaded correctly.
    """
    # Arrange
    storage = temp_storage
    test_name = "test_normalized_data"
    test_data = [
        NormalizedVacancy(id="1", title="Dev", url="http://a.com", source="test"),
        NormalizedVacancy(
            id="2", title="Eng", url="http://b.com", source="test", skills=["python"]
        ),
    ]

    # Act
    storage.save_normalized(test_name, test_data)
    loaded_data = storage.load_normalized(test_name)

    # Assert
    assert loaded_data == test_data


def test_load_raises_file_not_found(temp_storage: LocalStorage):
    """
    Verify that loading a non-existent file raises FileNotFoundError.
    """
    # Arrange
    storage = temp_storage

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        storage.load_raw("non_existent_file")

    with pytest.raises(FileNotFoundError):
        storage.load_normalized("non_existent_file")


def test_save_raw_creates_file(temp_storage: LocalStorage):
    """
    Verify that save_raw actually creates a file in the correct location.
    """
    # Arrange
    storage = temp_storage
    test_name = "raw_file_creation"
    test_data = {"status": "created"}
    from skillradar.core.storage import paths

    expected_file = paths.RAW_DIR / f"{test_name}.json"

    # Act
    storage.save_raw(test_name, test_data)

    # Assert
    assert expected_file.exists()
    assert expected_file.is_file()
    with open(expected_file, "r") as f:
        content = json.load(f)
    assert content == test_data


def test_save_and_load_raw_vacancy_list(temp_storage: LocalStorage):
    """
    Verify that save_raw correctly handles a list of RawVacancy dataclasses.
    """
    # Arrange
    storage = temp_storage
    test_name = "test_raw_vacancies"
    test_data = [
        RawVacancy(
            id="1",
            name="Python Dev",
            key_skills=["python", "django"],
            # alternate_url is optional but not explicitly None here
        ),
        RawVacancy(
            id="2",
            name="Go Dev",
            area={"name": "Remote"},
            # alternate_url is optional but not explicitly None here
        ),
    ]

    # Act
    storage.save_raw(test_name, test_data)
    loaded_data = storage.load_raw(test_name)

    # Assert
    expected_data = [asdict(v) for v in test_data]
    assert loaded_data == expected_data


def test_save_and_load_raw_vacancy_with_optional_fields(temp_storage: LocalStorage):
    """
    Verify that save_raw correctly handles RawVacancy objects
    where optional fields are missing or None.
    """
    # Arrange
    storage = temp_storage
    test_name = "test_raw_vacancies_optional"
    test_data = [
        RawVacancy(
            id="3",
            name="Frontend Dev",
            # description, branded_description, key_skills, area are all None/default
        ),
        RawVacancy(
            id="4",
            name="Backend Dev",
            description="A very interesting role.",
            key_skills=["java"],
            area={"name": "Hybrid"},
            branded_description=None,  # Explicitly None
        ),
    ]

    # Act
    storage.save_raw(test_name, test_data)
    loaded_data = storage.load_raw(test_name)

    # Assert
    expected_data = [asdict(v) for v in test_data]
    assert loaded_data == expected_data


def test_save_and_load_raw_vacancy_with_empty_id(temp_storage: LocalStorage):
    """
    Verify that save_raw correctly handles RawVacancy objects with an empty string ID.
    """
    # Arrange
    storage = temp_storage
    test_name = "test_raw_vacancy_empty_id"
    test_data = [
        RawVacancy(
            id="",  # Empty ID
            name="Vacancy with no ID",
            description="This is a test vacancy with an empty ID.",
        ),
    ]

    # Act
    storage.save_raw(test_name, test_data)
    loaded_data = storage.load_raw(test_name)

    # Assert
    expected_data = [asdict(v) for v in test_data]
    assert loaded_data == expected_data

