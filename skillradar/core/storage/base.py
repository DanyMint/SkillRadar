"""Defines the abstract base class for storage operations.

This module provides the Storage ABC, which declares the contract
for all storage implementations. It ensures that any storage backend
will have a consistent interface for saving and loading raw data.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union


class Storage(ABC):
    """Abstract base class for data storage."""

    @abstractmethod
    def ensure_dirs(self) -> None:
        """
        Ensures that the necessary directories for the storage exist.
        This should be called lazily when data is first written.
        """
        raise NotImplementedError

    @abstractmethod
    def save_raw(self, name: str, data: Union[Dict[str, Any], List[Any]]) -> None:
        """
        Saves raw data (e.g., from an API response) to the storage.

        Args:
            name: A unique identifier for the data (e.g., 'vacancies_2025-12-20').
            data: The Python object (dict or list) to be stored.
        """
        raise NotImplementedError

    @abstractmethod
    def load_raw(self, name: str) -> Union[Dict[str, Any], List[Any]]:
        """
        Loads raw data from the storage.

        Args:
            name: The unique identifier for the data to load.

        Returns:
            The loaded Python object.

        Raises:
            FileNotFoundError: If the data with the given name does not exist.
        """
        raise NotImplementedError
