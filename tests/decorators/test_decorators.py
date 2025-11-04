import sys
from pathlib import Path

# Ensure project root is on sys.path so `src` package can be imported when running tests directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from unittest.mock import patch
import pytest
from fastapi import HTTPException

from src.decorators import require_dev_environment


def test_decorator_allows_in_dev():
    """When ENVIRONMENT == 'dev', the decorated function should run normally."""
    with patch('src.decorators.param_store.get_secret', return_value='dev'):
        @require_dev_environment
        def sample(a, b=2):
            return a + b

        assert sample(3) == 5
        # metadata preserved
        assert sample.__name__ == 'sample'


def test_decorator_blocks_non_dev():
    """When ENVIRONMENT != 'dev', the decorator should raise HTTPException(403)."""
    with patch('src.decorators.param_store.get_secret', return_value='prod'):
        @require_dev_environment
        def sample():
            return 'allowed'

        with pytest.raises(HTTPException) as excinfo:
            sample()

        assert excinfo.value.status_code == 403
        assert 'Not Authorized' in str(excinfo.value.detail)


def test_decorator_passes_kwargs_and_args():
    """Ensure the decorator forwards args and kwargs to the wrapped function."""
    with patch('src.decorators.param_store.get_secret', return_value='dev'):
        @require_dev_environment
        def sample(x, y=10, z=None):
            return x, y, z

        assert sample(1, y=2, z=3) == (1, 2, 3)

