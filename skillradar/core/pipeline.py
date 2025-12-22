from datetime import datetime
from typing import List

from .fetch.base import VacancyFetcher
from .storage.base import Storage
from .normalize.base import BaseNormalizer
from .normalize.models import NormalizedVacancy


class Pipeline:
    def __init__(self, fetcher: VacancyFetcher, normalizer: BaseNormalizer, storage: Storage):
        self.fetcher = fetcher
        self.normalizer = normalizer
        self.storage = storage

    def run(self, **kwargs) -> List[NormalizedVacancy]:
        raw_vacancies = self.fetcher.fetch(**kwargs)

        # Сохраняем raw данные
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"vacancies_{timestamp}"
        self.storage.save_raw(file_name, raw_vacancies)

        # Нормализация
        normalized_vacancies: List[NormalizedVacancy] = []
        for raw_vacancy in raw_vacancies:
            try:
                normalized_vacancies.append(self.normalizer.normalize(raw_vacancy))
            except ValueError as e:
                print(f"Error normalizing vacancy {raw_vacancy.get('id')}: {e}")
                # Optionally, log the error or handle it differently

        # TODO: дальше будут extract, analyze
        return normalized_vacancies
