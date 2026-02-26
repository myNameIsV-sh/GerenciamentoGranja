from unittest.mock import Mock
from app.services.GalpaoService import GalpaoService

class TestGalpaoService:

    @pytest.fixture
    def galpao_repo_mock(self):
        return Mock()

    @pytest.fixture
    def galpao_service(self, galpao_repo_mock):
        return GalpaoService(galpao_repo_mock)

    def test_erro_not_found(self, galpao_service, galpao_repo_mock):
        # Simula o banco não encontrando o galpão
        galpao_repo_mock.get_by_id.return_value = None