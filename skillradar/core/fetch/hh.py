from .base import VacancyFetcher, RegionFetcher, fetch_exceptions

import requests

BASE_URL = "https://api.hh.ru/" 

class HHFetcher(VacancyFetcher):
    
    @fetch_exceptions
    def fetch(self, *, role:str, region:str, limit:int=1000) -> list[dict]:
        params = {
            "per_page": 20, 
            "text":role,
            }

        url = BASE_URL + "vacancies"   
        r = requests.get(url, params)
        r.raise_for_status()
        return r.json()


class HHRegionFetcher(RegionFetcher):
    @fetch_exceptions
    def fetch(self) -> list[dict]:
        url = BASE_URL + "areas"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()