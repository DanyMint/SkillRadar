from .base import VacancyFetcher, RegionFetcher, fetch_exceptions

import requests

BASE_URL = "https://api.hh.ru/" 

class HHFetcher(VacancyFetcher):
    """
    Класс для получения вакансий с HeadHunter API.
    """

    @fetch_exceptions
    def fetch(self, search_query: str, region_id: int, total_vacancies: int) -> list[dict]:
        """
        Собирает вакансии с HeadHunter API с учетом пагинации.

        Args:
            search_query: Поисковый запрос (название вакансии, ключевые слова).
            region_id: ID региона для поиска.
            total_vacancies: Желаемое количество вакансий для получения.

        Returns:
            Список словарей, где каждый словарь представляет вакансию.
        """
        vacancies = []
        per_page = 100  # Максимальное количество вакансий на странице
        page = 0

        while len(vacancies) < total_vacancies:
            params = {
                "text": search_query,
                "area": region_id,
                "per_page": per_page,
                "page": page,
                "search_field": ["name", "description"],
            }
            
            url = BASE_URL + "vacancies"
            r = requests.get(url, params)
            r.raise_for_status()
            data = r.json()
            
            items = data.get("items", [])
            if not items:
                break  # Больше вакансий нет

            vacancies.extend(items)
            page += 1
            
            # Если API вернуло меньше страниц, чем есть на самом деле
            if page >= data.get("pages", page):
                break

        return vacancies[:total_vacancies]


class HHRegionFetcher(RegionFetcher):
    @fetch_exceptions
    def fetch(self) -> list[dict]:
        url = BASE_URL + "areas"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()