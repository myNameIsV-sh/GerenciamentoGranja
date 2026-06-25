import pytest
from unittest.mock import Mock, patch
from app.services.LoteService import LoteService


class TestLoteService:

    @pytest.fixture
    def dependencias(self):
        return {
            "lote_repo": Mock(),
            "galpao_service": Mock()
        }

    @pytest.fixture
    def lote_service(self, dependencias):
        return LoteService(dependencias["lote_repo"], dependencias["galpao_service"])

    @patch('app.services.AlimentacaoService.AlimentacaoService.analisar_consumo')
    @patch('app.services.FotoPeriodoService.FotoPeriodoService.obter_configuracao_semanal')
    def test_calculo_populacao_e_orquestracao(self, mock_obter_luz, mock_analisar_consumo, lote_service, dependencias):
        # 1. Configurar o Lote falso
        mock_lote = Mock()
        mock_lote.calcular_idade_em_semanas = 4
        mock_lote.quantidade_inicial_aves = 10000
        mock_lote.mortalidade_acumulada = 200
        mock_lote.consumo_total_racao_kg = 500.0
        mock_lote.id_galpao = 10

        dependencias["lote_repo"].get_lote.return_value = mock_lote
        mock_analisar_consumo.return_value = {"status": "Adequado"}
        mock_obter_luz.return_value = {"luz": "configurada"}

        # 2. Executar a ação
        resultado = lote_service.registrar_consumo_semanal(id_lote=1, racao_consumida_kg=100.0)

        # 3. Asserts
        mock_analisar_consumo.assert_called_once_with(4, 100.0, 9800)
        mock_obter_luz.assert_called_once_with(4)
        dependencias["galpao_service"].atualizar_configuracao_luz.assert_called_once_with(10, {"luz": "configurada"})
        assert mock_lote.consumo_total_racao_kg == 600.0
        assert resultado["analise_alimentacao"]["status"] == "Adequado"

    def test_lote_inexistente(self, lote_service, dependencias):
        dependencias["lote_repo"].get_lote.side_effect = Exception("Erro 404: Lote não encontrado")

        with pytest.raises(Exception, match="404: Lote não encontrado"):
            lote_service.registrar_consumo_semanal(id_lote=999, racao_consumida_kg=50.0)

