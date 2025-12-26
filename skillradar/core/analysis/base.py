from abc import ABC, abstractmethod

from .models import AnalysisResult


class BaseAnalyzer(ABC):
    """
    Абстрактный базовый класс для анализаторов текста вакансии.
    """

    @abstractmethod
    def analyze(self, vacancy_id: str, text: str) -> AnalysisResult:
        """
        Анализирует текст и возвращает результат.
        """
        raise NotImplementedError
