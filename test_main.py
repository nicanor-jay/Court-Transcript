import pytest
from main import dummy_function


def test_dummy_function():
    """Tests the dummy function from main."""
    assert dummy_function("Jon Wick")
