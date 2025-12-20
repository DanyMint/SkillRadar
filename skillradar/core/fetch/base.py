import functools
from abc import ABC, abstractmethod
from requests.exceptions import ConnectionError, RequestException, Timeout

class VacancyFetcher(ABC):
    @abstractmethod
    
    def fetch(self, *,search_query: str, region_id: int, total_vacancies: int) -> list[dict]:
        pass

class RegionFetcher(ABC):
    @abstractmethod
    def fetch(self) -> list[dict]:
        pass

def fetch_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            return {"error": "Нет сети"}
        except Timeout:
            return {"error": "Превышено время ожидания"}
        except RequestException as e:
            return {"error": f"Ошибка запроса: {str(e)}"}
        except ValueError:
            return {"error": "Ошибка парсинга JSON"}
    return wrapper