"""Local file system storage implementation."""
import json
from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List, Union

from ..normalize.models import NormalizedVacancy
from . import paths
from .base import Storage


class LocalStorage(Storage):
    """
    Stores pipeline artifacts (raw, normalized data, etc.) on the
    local file system as JSON files.
    """

    def ensure_dirs(self) -> None:
        """
        Creates the directories for all data types if they don't exist.
        The creation is recursive and suppresses errors if directories already exist.
        """
        paths.RAW_DIR.mkdir(parents=True, exist_ok=True)
        paths.NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)

    def save_raw(self, name: str, data: Union[Dict[str, Any], List[Any]]) -> None:
        """
        Saves a Python object as a JSON file in the raw data directory.

        If the data is a list of dataclass objects, they are converted to
        dictionaries before serialization.

        The method ensures the target directory exists before writing.
        Files are saved with UTF-8 encoding and without escaping non-ASCII chars.

        Args:
            name: The base name for the file (e.g., 'vacancies_hh').
                  '.json' extension will be appended.
            data: The dictionary or list to save.
        """
        self.ensure_dirs()
        file_path = paths.RAW_DIR / f"{name}.json"

        # Prepare data for JSON serialization (handle list of dataclasses)
        json_data = data
        if isinstance(data, list) and data and is_dataclass(data[0]):
            json_data = [asdict(item) for item in data]

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

    def load_raw(self, name: str) -> Union[Dict[str, Any], List[Any]]:
        """
        Loads a JSON file from the raw data directory into a Python object.

        Args:
            name: The base name of the file to load.

        Returns:
            The loaded data as a dictionary or list.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        file_path = paths.RAW_DIR / f"{name}.json"
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_normalized(self, name: str, data: List[NormalizedVacancy]) -> None:
        """
        Saves a list of normalized vacancies as a JSON file in the normalized
        data directory.

        The Pydantic models are converted to dictionaries before serialization.

        Args:
            name: The base name for the file. '.json' will be appended.
            data: The list of NormalizedVacancy objects to save.
        """
        self.ensure_dirs()
        file_path = paths.NORMALIZED_DIR / f"{name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json_data = [asdict(vacancy) for vacancy in data]
            json.dump(json_data, f, ensure_ascii=False, indent=2)

    def load_normalized(self, name: str) -> List[NormalizedVacancy]:
        """
        Loads a JSON file from the normalized data directory into a list of
        NormalizedVacancy objects.

        Args:
            name: The base name of the file to load.

        Returns:
            The loaded data as a list of NormalizedVacancy objects.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        file_path = paths.NORMALIZED_DIR / f"{name}.json"
        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            return [NormalizedVacancy(**item) for item in json_data]
