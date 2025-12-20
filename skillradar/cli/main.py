from skillradar.core.fetch.hh import HHFetcher
from skillradar.core.pipeline import Pipeline
from skillradar.core.storage.local import LocalStorage


def main():
    # config = parse_args()  # Предполагается, что здесь будет парсинг аргументов

    # 1. Создание зависимостей
    fetcher = HHFetcher()
    storage = LocalStorage()

    # 2. Внедрение зависимостей в Pipeline
    pipeline = Pipeline(fetcher=fetcher, storage=storage)

    # 3. Запуск pipeline с параметрами
    # В реальном приложении параметры придут из config
    vacancies = pipeline.run(search_query="Python developer", region_id="1", total_vacancies=5)

    print(f"Successfully fetched and saved {len(vacancies)} vacancies.")


if __name__ == "__main__":
    main()
