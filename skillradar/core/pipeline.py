class Pipeline:
    def __init__(self, fetcher):
        self.fetcher = fetcher

    def run(self, config):
        vacancies = self.fetcher.fetch(
            role=config.role,
            region=config.region,
            limit=config.limit,
        )

        # дальше будут normalize, extract, analyze
        return vacancies
