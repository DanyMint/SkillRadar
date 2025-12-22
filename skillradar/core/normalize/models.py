from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class NormalizedVacancy:
    """A canonical representation of a vacancy."""

    id: str
    title: str
    url: str
    source: str

    company_name: Optional[str] = None
    description: Optional[str] = None
    skills: List[str] = field(default_factory=list)

    location: Optional[str] = None
