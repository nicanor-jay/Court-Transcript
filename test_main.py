import pytest
from main import dummy_function

# pylint: skip-file


def test_dummy_function():
    """Tests the dummy function from main."""
    assert dummy_function("Jon Wick")
