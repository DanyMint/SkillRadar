from skillradar.core.normalize.hh import HhNormalizer
from skillradar.core.normalize.models import NormalizedVacancy
import pytest

def test_hh_normalizer_basic_data():
    raw_data = {
        "id": "12345",
        "name": "Python Developer",
        "area": {
            "id": "1",
            "name": "Москва",
            "url": "https://api.hh.ru/areas/1"
        },
        "published_at": "2023-01-15T10:00:00+0300",
        "description": "<p>Awesome Python job.</p>",
        "branded_description": None,
        "key_skills": [
            {"name": "Python"},
            {"name": "Django"},
            {"name": "SQL"}
        ],
        "raw": { # This 'raw' field mimics the full details from HH API
            "id": "12345",
            "name": "Python Developer",
            "description": "<p>Awesome Python job.</p>",
            "employer": {
                "id": "6789",
                "name": "Great Company",
                "url": "https://api.hh.ru/employers/6789",
                "alternate_url": "https://hh.ru/employer/6789"
            },
            "area": {
                "id": "1",
                "name": "Москва",
                "url": "https://api.hh.ru/areas/1"
            },
            "key_skills": [
                {"name": "Python"},
                {"name": "Django"},
                {"name": "SQL"}
            ],
            "alternate_url": "https://hh.ru/vacancy/12345"
        }
    }

    normalizer = HhNormalizer()
    normalized_vacancy = normalizer.normalize(raw_data)

    assert isinstance(normalized_vacancy, NormalizedVacancy)
    assert normalized_vacancy.id == "12345"
    assert normalized_vacancy.title == "Python Developer"
    assert normalized_vacancy.url == "https://hh.ru/vacancy/12345"
    assert normalized_vacancy.source == "HeadHunter"
    assert normalized_vacancy.company_name == "Great Company"
    assert normalized_vacancy.description == "<p>Awesome Python job.</p>"
    assert normalized_vacancy.skills == ["Python", "Django", "SQL"]
    assert normalized_vacancy.location == "Москва"

def test_hh_normalizer_missing_optional_fields():
    raw_data = {
        "id": "67890",
        "name": "Junior Developer",
        "area": {}, # Missing area name
        "published_at": "2023-01-16T12:00:00+0300",
        "description": "<p>A junior role.</p>",
        "branded_description": None,
        "key_skills": [], # No skills
        "raw": { # 'raw' might also be sparse
            "id": "67890",
            "name": "Junior Developer",
            "description": "<p>A junior role.</p>",
            "employer": {}, # Missing employer name
            "area": {},
            "key_skills": [],
            "alternate_url": "https://hh.ru/vacancy/67890"
        }
    }

    normalizer = HhNormalizer()
    normalized_vacancy = normalizer.normalize(raw_data)

    assert isinstance(normalized_vacancy, NormalizedVacancy)
    assert normalized_vacancy.id == "67890"
    assert normalized_vacancy.title == "Junior Developer"
    assert normalized_vacancy.url == "https://hh.ru/vacancy/67890"
    assert normalized_vacancy.source == "HeadHunter"
    assert normalized_vacancy.company_name is None # Should be None
    assert normalized_vacancy.description == "<p>A junior role.</p>"
    assert normalized_vacancy.skills == [] # Should be empty list
    assert normalized_vacancy.location is None # Should be None

def test_hh_normalizer_missing_required_fields():
    raw_data = {
        "id": None, # Missing ID
        "name": "Incomplete Vacancy",
        "raw": {}
    }
    normalizer = HhNormalizer()
    with pytest.raises(ValueError, match="Missing required fields for normalization"):
        normalizer.normalize(raw_data)

def test_hh_normalizer_description_combination():
    raw_data = {
        "id": "789",
        "name": "Test Desc",
        "area": {},
        "description": "Main description.", # This comes from _parse_vacancy output
        "branded_description": "Branded description from full details.", # This too
        "key_skills": [],
        "raw": { # Full details
            "id": "789",
            "name": "Test Desc",
            "description": "Main description.", # This should match raw_data['description']
            "branded_description": "Branded description from full details.", # This should match raw_data['branded_description']
            "employer": {"name": "Test Employer"},
            "alternate_url": "https://hh.ru/vacancy/789"
        }
    }
    normalizer = HhNormalizer()
    normalized_vacancy = normalizer.normalize(raw_data)
    assert normalized_vacancy.description == "Main description.\n\n---\n\nBranded description from full details."
    assert normalized_vacancy.company_name == "Test Employer"

def test_hh_normalizer_description_fallback_from_raw():
    raw_data = {
        "id": "888",
        "name": "No desc in main",
        "area": {},
        "description": "", # Empty in _parse_vacancy output
        "branded_description": None,
        "key_skills": [],
        "raw": {
            "id": "888",
            "name": "No desc in main",
            "description": "Description only in raw details.", # Present here
            "employer": {"name": "Another Employer"},
            "alternate_url": "https://hh.ru/vacancy/888"
        }
    }
    normalizer = HhNormalizer()
    normalized_vacancy = normalizer.normalize(raw_data)
    assert normalized_vacancy.description == "Description only in raw details."
    assert normalized_vacancy.company_name == "Another Employer"
