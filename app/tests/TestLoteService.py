from unittest.mock import Mock, patch
from app.services.LoteService import LoteService

class TestLoteService:

    @pytest.fixture
    def dependencias(self):
        # Retorna os mocks que injetaremos no LoteService
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
        # 1. Configurar o Lote falso retornado pelo repositório
        mock_lote = Mock()
        mock_lote.calcular_idade_em_semanas = 4
        mock_lote.quantidade_inicial_aves = 10000
        mock_lote.mortalidade_acumulada = 200
        mock_lote.consumo_total_racao_kg = 500.0
        mock_lote.id_galpao = 10
        
        dependencias["lote_repo"].get_lote.return_value = mock_lote
        
        # Configurar retornos falsos para os métodos de classe patcheados
        mock_analisar_consumo.return_value = {"status": "Adequado"}
        mock_obter_luz.return_value = {"luz": "configurada"}
        
        # 2. Executar a ação
        resultado = lote_service.registrar_consumo_semanal(id_lote=1, racao_consumida_kg=100.0)
        
        # 3. Verificações (Asserts)
        # Teste de Cálculo de População: 10000 - 200 = 9800
        mock_analisar_consumo.assert_called_once_with(4, 100.0, 9800)
        
        # Teste de Orquestração
        mock_obter_luz.assert_called_once_with(4)
        dependencias["galpao_service"].atualizar_configuracao_luz.assert_called_once_with(10, {"luz": "configurada"})
        
        # Verifica se o consumo foi somado e o lote salvo
        assert mock_lote.consumo_total_racao_kg == 600.0
        dependencias["lote_repo"].save.assert_called_once_with(mock_lote)
        
        # Verifica retorno final
        assert resultado["analise_alimentacao"]["status"] == "Adequado"