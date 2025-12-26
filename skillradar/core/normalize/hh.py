from typing import Any, Dict, Optional
from skillradar.core.normalize.base import BaseNormalizer
from skillradar.core.normalize.models import NormalizedVacancy

class HhNormalizer(BaseNormalizer):
    def normalize(self, raw_data: Dict[str, Any]) -> NormalizedVacancy:
        # The input raw_data is the output of HHFetcher._parse_vacancy
        # The actual full details from the HH API are often stored under the 'raw' key
        full_details = raw_data.get("raw", {})

        vacancy_id: Optional[str] = None
        url: Optional[str] = None

        original_id = raw_data.get("id")
        if original_id is not None:
            vacancy_id = str(original_id)
            url = f"https://hh.ru/vacancy/{vacancy_id}"

        title = raw_data.get("name")
        
        # Extract company name from the 'employer' details within the full raw data
        company_name = full_details.get("employer", {}).get("name")

        # Description handling
        # Prefer description from full_details, which is typically the most complete
        full_description = full_details.get("description", "") 
        branded_description = full_details.get("branded_description", "") 
        
        # If there's a branded description and it's different from the main description, combine them
        if branded_description and branded_description != full_description:
            if full_description:
                full_description = f"{full_description}\n\n---\n\n{branded_description}"
            else: # If main description was empty, but branded exists
                full_description = branded_description
        
        # Fallback: if no description found yet, try raw_data.description
        if not full_description.strip() and raw_data.get("description"):
            full_description = raw_data.get("description")

        # Extract skills - now correctly extracting the 'name' from each skill dict
        skills = [skill.get("name") for skill in raw_data.get("key_skills", []) if isinstance(skill, dict) and skill.get("name")]

        # Extract location name - _parse_vacancy already extracts area name
        location = raw_data.get("area", {}).get("name")

        # Basic validation for required fields
        if not vacancy_id or not title or not url:
            raise ValueError(f"Missing required fields for normalization: id={vacancy_id}, title={title}, url={url}")

        return NormalizedVacancy(
            id=vacancy_id,
            title=title,
            url=url,
            source="HeadHunter",
            company_name=company_name,
            description=full_description,
            skills=skills,
            location=location,
        )
