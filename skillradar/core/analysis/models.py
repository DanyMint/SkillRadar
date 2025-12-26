from dataclasses import dataclass, field
from typing import Any


@dataclass
class AnalysisResult:
    """
    Результат анализа текста вакансии.
    """

    vacancy_id: str
    data: dict[str, Any] = field(default_factory=dict)
