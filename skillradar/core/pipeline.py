from datetime import datetime

from .fetch.base import VacancyFetcher
from .storage.base import Storage


class Pipeline:
    def __init__(self, fetcher: VacancyFetcher, storage: Storage):
        self.fetcher = fetcher
        self.storage = storage

    def run(self, **kwargs):
        vacancies = self.fetcher.fetch(**kwargs)

        # Сохраняем raw данные
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"vacancies_{timestamp}"
        self.storage.save_raw(file_name, vacancies)

        # дальше будут normalize, extract, analyze
        return vacancies
