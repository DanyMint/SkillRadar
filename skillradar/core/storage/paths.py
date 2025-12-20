"""Defines the application's file system paths.

This module uses pathlib for cross-platform compatibility.
Paths are defined for the application's root directory, data directory,
and raw data directory within the user's home directory.
"""
from pathlib import Path

# ~/.skillradar
APP_DIR: Path = Path.home() / ".skillradar"

# ~/.skillradar/data
DATA_DIR: Path = APP_DIR / "data"

# ~/.skillradar/data/raw
RAW_DIR: Path = DATA_DIR / "raw"
