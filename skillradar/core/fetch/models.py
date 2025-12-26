from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RawVacancy:
    """
    A data class representing a single raw vacancy listing
    as fetched from an external source (e.g., HeadHunter API).

    This is a lean version that only stores fields required for
    the normalization process, optimizing for storage space.
    """

    id: str
    name: str  # Will be mapped to 'title'
    
    # Fields for normalization
    description: Optional[str] = None
    branded_description: Optional[str] = None
    key_skills: List[str] = field(default_factory=list)
    area: Optional[Dict[str, Any]] = None  # For 'location'
