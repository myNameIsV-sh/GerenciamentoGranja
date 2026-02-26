import sys
import os

# Adiciona a pasta raiz ao sys.path para que 'app.services' seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_lote_repository():
    """Fixture para simular o repositório de lotes"""
    return Mock()

@pytest.fixture
def mock_galpao_service():
    """Fixture para simular o serviço de galpão"""
    return Mock()