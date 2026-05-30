"""Shared pytest fixtures."""
import numpy as np
import pytest

@pytest.fixture
def s():
    """Sympy symbol `s` for transfer-function expressions."""
    import sympy
    return sympy.Symbol("s")
