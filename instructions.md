# instructions.md

## Project Overview

SkillRadar is a Python project that generates an HTML report showing current job market demand for skills based on real vacancies.

The project is structured into three main components:
- `cli`: Handles the command-line interface and user input.
- `core`: Contains the main business logic, including the data processing pipeline and fetching from job sites.
    - `fetch`: Contains modules for fetching data from different job sites. Currently, only HeadHunter (`hh.ru`) is supported.
    - `storage`: Provides a simple abstraction for storing and retrieving data. The local file system is used as the default storage.
- `data`: Stores raw and processed data.

The main technologies used are:
- Python 3.13+
- `requests` for making HTTP requests to job site APIs.

## Building and Running

The project uses `uv` for dependency management.

**Installation:**
```bash
uv pip install -e .
```

**Running the application:**
```bash
skillradar
```
Currently, the application is in the early stages of development and the main entry point `skillradar/cli/main.py` is not fully implemented.

**Running tests:**
There are no tests in the project yet.

## Development Conventions

The project follows a standard Python project structure.

- The core logic is separated from the command-line interface.
- The project uses type hints.

### Fetchers

Fetchers for different job sites should inherit from `VacancyFetcher` or `RegionFetcher` in `skillradar/core/fetch/base.py`.

- `VacancyFetcher`: Implement the `fetch` method to retrieve a list of vacancies.
- `RegionFetcher`: Implement the `fetch` method to retrieve a list of regions.

It is recommended to use the `@fetch_exceptions` decorator to handle common request exceptions.

### Storage

Storage backends should inherit from the `Storage` class in `skillradar/core/storage/base.py`. Implement the `save_raw` and `load_raw` methods to handle data storage.
