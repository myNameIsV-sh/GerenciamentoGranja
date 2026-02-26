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
        
        with pytest.raises(ValueError, match="não foi encontrado"):
            galpao_service.obter_galpao_por_id(999)
            
    def test_status_invalido(self, galpao_service, galpao_repo_mock):
        # Simula um galpão existente
        galpao_repo_mock.get_by_id.return_value = Mock()
        
        # Garante que o ValueError é levantado para status não permitidos
        with pytest.raises(ValueError, match="Status inválido"):
            galpao_service.atualizar_status_ocupacao(1, "Pegando Fogo")