from typing import Any, Dict, List, Optional

import requests

from .base import RegionFetcher, VacancyFetcher, fetch_exceptions

BASE_URL = "https://api.hh.ru/"


class HHFetcher(VacancyFetcher):
    """
    Класс для получения вакансий с HeadHunter API.

    Получает детальную информацию по каждой вакансии,
    включая описание и ключевые навыки.
    """

    @fetch_exceptions
    def fetch(
        self,
        *,
        search_query: str,
        total_vacancies: int,
        region_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Собирает вакансии с HeadHunter API с учетом пагинации и обогащения.

        Args:
            search_query: Поисковый запрос (название вакансии, ключевые слова).
            total_vacancies: Желаемое количество вакансий для получения.
            region_id: ID региона для поиска (опционально).

        Returns:
            Список словарей, где каждый словарь представляет обогащенную вакансию.
        """
        vacancies = []
        per_page = 100
        page = 0

        while len(vacancies) < total_vacancies:
            params: Dict[str, Any] = {
                "text": search_query,
                "per_page": per_page,
                "page": page,
                "search_field": ["name", "description"],
            }
            if region_id:
                params["area"] = region_id

            r = requests.get(f"{BASE_URL}vacancies", params)
            r.raise_for_status()
            data = r.json()

            found_items = data.get("items", [])
            if not found_items:
                break

            for item in found_items:
                if len(vacancies) >= total_vacancies:
                    break
                details = self._get_vacancy_details(item["id"])
                if details:
                    vacancies.append(self._parse_vacancy(details))

            page += 1
            if page >= data.get("pages", page):
                break

        return vacancies[:total_vacancies]

    @fetch_exceptions
    def _get_vacancy_details(self, vacancy_id: str) -> Optional[Dict[str, Any]]:
        """Получает полную информацию о вакансии по ее ID."""
        r = requests.get(f"{BASE_URL}vacancies/{vacancy_id}")
        r.raise_for_status()
        return r.json()

    def _parse_vacancy(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """Приводит детальную информацию о вакансии к нужной структуре."""
        return {
            "id": details.get("id"),
            "name": details.get("name"),
            "area": details.get("area"),
            "published_at": details.get("published_at"),
            "description": details.get("description"),
            "branded_description": details.get("branded_description"),
            "key_skills": [skill["name"] for skill in details.get("key_skills", [])],
            "raw": details,
        }


class HHRegionFetcher(RegionFetcher):
    @fetch_exceptions
    def fetch(self) -> List[Dict[str, Any]]:
        r = requests.get(f"{BASE_URL}areas")
        r.raise_for_status()
        return r.json()
