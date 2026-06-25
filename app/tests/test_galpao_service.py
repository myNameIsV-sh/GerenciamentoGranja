import pytest
from unittest.mock import Mock, patch
from app.services.GalpaoService import GalpaoService


class TestGalpaoService:

    @pytest.fixture
    def galpao_repo_mock(self):
        return Mock()

    @pytest.fixture
    def galpao_service(self, galpao_repo_mock):
        return GalpaoService(galpao_repo_mock)

    def test_erro_not_found(self, galpao_service, galpao_repo_mock):
        galpao_repo_mock.get_by_id.return_value = None

        with pytest.raises(ValueError, match="não foi encontrado"):
            galpao_service.obter_galpao_por_id(999)

    def test_status_invalido(self, galpao_service, galpao_repo_mock):
        galpao_repo_mock.get_by_id.return_value = Mock()

        with pytest.raises(ValueError, match="Status inválido"):
            galpao_service.atualizar_status_ocupacao(1, "Status Fantasia")

    def test_atualizacao_de_luz(self, galpao_service, galpao_repo_mock):
        mock_galpao = Mock()
        galpao_repo_mock.get_by_id.return_value = mock_galpao

        config_luz = {
            "horario_religamento_luzes": "18:00",
            "horario_desligamento_luzes": "06:00"
        }

        galpao_service.atualizar_configuracao_luz(1, config_luz)

        assert mock_galpao.horario_religamento_luzes == "18:00"
        assert mock_galpao.horario_desligamento_luzes == "06:00"
        galpao_repo_mock.save.assert_called_once_with(mock_galpao)

    def test_registrar_temperatura_atual(self, galpao_service, galpao_repo_mock):
        mock_galpao = Mock()
        galpao_repo_mock.get_by_id.return_value = mock_galpao

        galpao_service.registrar_temperatura_atual(1, 28.5)

        assert mock_galpao.temperatura_atual == 28.5
        galpao_repo_mock.save.assert_called_once_with(mock_galpao)

    def test_listar_todos(self, galpao_service, galpao_repo_mock):
        galpao_repo_mock.listar_todos.return_value = [{"id": 1, "status": "Livre"}]
        resultado = galpao_service.listar_todos()
        assert len(resultado) == 1
        galpao_repo_mock.listar_todos.assert_called_once()

    @patch('app.models.Galpao.Galpao')
    def test_criar_galpao(self, mock_galpao_model, galpao_service, galpao_repo_mock):
        dados = {"identificacao": "G1", "status": "Livre"}
        mock_instancia = Mock()
        mock_galpao_model.return_value = mock_instancia
        galpao_repo_mock.save.return_value = mock_instancia

        resultado = galpao_service.criar_galpao(dados)

        galpao_repo_mock.save.assert_called_once_with(mock_instancia)
        assert resultado == mock_instancia

    def test_atualizar_galpao(self, galpao_service, galpao_repo_mock):
        mock_galpao = Mock()
        galpao_repo_mock.get_by_id.return_value = mock_galpao

        galpao_service.atualizar_galpao(1, {"temperatura_atual": 26.0})

        assert mock_galpao.temperatura_atual == 26.0
        galpao_repo_mock.save.assert_called_once_with(mock_galpao)

    def test_deletar_galpao_sucesso(self, galpao_service, galpao_repo_mock):
        # 1. Configuramos um galpão existente
        mock_galpao = Mock()
        galpao_repo_mock.get_by_id.return_value = mock_galpao

        # 2. IMPORTANTE: Simulamos que a lista de lotes vinculados está VAZIA
        # O service provavelmente checa algo como galpao.lotes
        mock_galpao.lotes = []

        # 3. Executamos a deleção
        galpao_service.deletar_galpao(1)

        # 4. Verificamos se o repositório foi chamado corretamente
        galpao_repo_mock.delete.assert_called_once_with(mock_galpao)

    def test_deletar_galpao_com_lote_erro(self, galpao_service, galpao_repo_mock):
        # Teste extra para validar que a sua trava de segurança FUNCIONA
        mock_galpao = Mock()
        galpao_repo_mock.get_by_id.return_value = mock_galpao

        # Simulamos que existe um lote na lista
        mock_galpao.lotes = [Mock()]

        with pytest.raises(ValueError, match="Não é possível deletar"):
            galpao_service.deletar_galpao(1)