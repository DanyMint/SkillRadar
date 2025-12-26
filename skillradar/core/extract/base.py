from abc import ABC, abstractmethod

from .models import ExtractionResult


class BaseExtractor(ABC):
    """
    Абстрактный базовый класс для извлечения навыков из текста.
    """

    @abstractmethod
    def extract(self, vacancy_id: str, text: str) -> ExtractionResult:
        """
        Извлекает навыки из текста и возвращает результат.
        """
        raise NotImplementedError
