"""
This __init__.py file makes the 'storage' directory a Python package
and exposes the primary classes for easier importing.
"""
from .base import Storage
from .local import LocalStorage

__all__ = ["Storage", "LocalStorage"]
