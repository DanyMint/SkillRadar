"""Local file system storage implementation."""
import json
from typing import Any, Dict, List, Union

from . import paths
from .base import Storage


class LocalStorage(Storage):
    """
    Stores data on the local file system as JSON files.
    """

    def ensure_dirs(self) -> None:
        """
        Creates the directory for raw data if it doesn't exist.
        The creation is recursive and suppresses errors if directories already exist.
        """
        paths.RAW_DIR.mkdir(parents=True, exist_ok=True)

    def save_raw(self, name: str, data: Union[Dict[str, Any], List[Any]]) -> None:
        """
        Saves a Python object as a JSON file in the raw data directory.

        The method ensures the target directory exists before writing.
        Files are saved with UTF-8 encoding and without escaping non-ASCII chars.

        Args:
            name: The base name for the file (e.g., 'vacancies_hh').
                  '.json' extension will be appended.
            data: The dictionary or list to save.
        """
        self.ensure_dirs()
        file_path = paths.RAW_DIR / f"{name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

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
