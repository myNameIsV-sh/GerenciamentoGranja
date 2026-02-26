import sys
import os
import pytest
from unittest.mock import Mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

@pytest.fixture
def mock_lote_repository():
    return Mock()

@pytest.fixture
def mock_galpao_service():
    return Mock()