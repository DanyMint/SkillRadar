"""Tests for the new methods in the LocalStorage class."""

import json
from dataclasses import asdict

import pytest

from skillradar.core.analysis.models import AnalysisResult
from skillradar.core.extract.models import ExtractionResult
from skillradar.core.storage import paths
from skillradar.core.storage.local import LocalStorage


@pytest.fixture
def storage():
    """Provides a LocalStorage instance for testing."""
    return LocalStorage()


def test_save_analysis(storage: LocalStorage):
    """
    Verify that the save_analysis method correctly saves an AnalysisResult
    object to a JSON file in the designated analysis directory.
    """
    # 1. Setup
    result = AnalysisResult(vacancy_id="test_vacancy_123", data={"foo": "bar"})
    expected_path = paths.ANALYSIS_DIR / f"{result.vacancy_id}.json"

    # Ensure no file exists before the test
    if expected_path.exists():
        expected_path.unlink()

    try:
        # 2. Execution
        storage.save_analysis(result)

        # 3. Verification
        assert expected_path.exists(), "The analysis file was not created."

        with open(expected_path, "r", encoding="utf-8") as f:
            saved_data = json.load(f)

        assert saved_data == asdict(
            result
        ), "The saved data does not match the original object."

    finally:
        # 4. Cleanup
        if expected_path.exists():
            expected_path.unlink()


def test_save_extraction(storage: LocalStorage):
    """
    Verify that the save_extraction method correctly saves an ExtractionResult
    object to a JSON file in the designated extraction directory.
    """
    # 1. Setup
    result = ExtractionResult(
        vacancy_id="test_vacancy_456", data=[{"skill": "Python"}]
    )
    expected_path = paths.EXTRACTION_DIR / f"{result.vacancy_id}.json"

    # Ensure no file exists before the test
    if expected_path.exists():
        expected_path.unlink()

    try:
        # 2. Execution
        storage.save_extraction(result)

        # 3. Verification
        assert expected_path.exists(), "The extraction file was not created."

        with open(expected_path, "r", encoding="utf-8") as f:
            saved_data = json.load(f)

        assert saved_data == asdict(
            result
        ), "The saved data does not match the original object."

    finally:
        # 4. Cleanup
        if expected_path.exists():
            expected_path.unlink()

