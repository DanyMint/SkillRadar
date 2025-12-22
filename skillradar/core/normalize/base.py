from abc import ABC, abstractmethod
from typing import Any, Dict

from skillradar.core.normalize.models import NormalizedVacancy


class BaseNormalizer(ABC):
    """Abstract base class for data normalizers."""

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> NormalizedVacancy:
        """
        Normalizes raw data into a NormalizedVacancy object.

        Args:
            raw_data: The raw JSON data (as a dict) from a specific source.

        Returns:
            A NormalizedVacancy object.
        """
        pass
