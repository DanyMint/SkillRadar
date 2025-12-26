from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExtractionResult:
    """
    Результат извлечения навыков из текста вакансии.
    """

    vacancy_id: str
    data: list[dict[str, Any]] = field(default_factory=list)
