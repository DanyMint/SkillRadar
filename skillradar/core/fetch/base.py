import functools
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from requests.exceptions import ConnectionError, RequestException, Timeout


class VacancyFetcher(ABC):
    @abstractmethod
    def fetch(
        self,
        *,
        search_query: str,
        total_vacancies: int,
        region_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        pass


class RegionFetcher(ABC):
    @abstractmethod
    def fetch(self) -> list[dict]:
        pass


class FetcherException(Exception):
    """Кастомное исключение для ошибок в fetcher'ах."""

    pass


def fetch_exceptions(func):
    """
    Декоратор для обработки исключений и перевыброса их
    в виде кастомного исключения FetcherException.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            raise FetcherException("Ошибка сети. Не удалось подключиться к серверу.") from e
        except Timeout as e:
            raise FetcherException("Превышено время ожидания ответа от сервера.") from e
        except RequestException as e:
            raise FetcherException(f"Произошла ошибка при выполнении запроса: {e}") from e
        except (ValueError, TypeError) as e:
            raise FetcherException("Ошибка парсинга ответа от сервера.") from e

    return wrapper