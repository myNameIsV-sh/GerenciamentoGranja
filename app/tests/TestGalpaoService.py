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
            
    def test_atualizacao_de_luz(self, galpao_service, galpao_repo_mock):
        mock_galpao = Mock()
        galpao_repo_mock.get_by_id.return_value = mock_galpao
        
        config_luz = {
            "horario_religamento_luzes": "18:00",
            "horario_desligamento_luzes": "06:00"
        }
        
        # Chama o serviço passando a configuração
        galpao_service.atualizar_configuracao_luz(1, config_luz)
        
        # Verifica se os atributos foram alterados corretamente
        assert mock_galpao.horario_religamento_luzes == "18:00"
        assert mock_galpao.horario_desligamento_luzes == "06:00"
        
        # Verifica se o método save do repositório foi chamado
        galpao_repo_mock.save.assert_called_once_with(mock_galpao)