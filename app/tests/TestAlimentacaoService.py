import pytest
from app.services.AlimentacaoService import AlimentacaoService

class TestAlimentacaoService:
    
    def test_limites_clamping(self):
        # Envia 0, deve corrigir para a semana 1
        meta_min = AlimentacaoService.obter_meta_semanal(0)
        assert meta_min["fase"] == "Adaptação"
        
        # Envia 30, deve travar na semana 18
        meta_max = AlimentacaoService.obter_meta_semanal(30)
        assert meta_max["racao_kg"] == 45.5
        
        
    def test_consumo_adequado(self):
        # Semana 1: meta base é 6.5kg. Para 1000 aves, o esperado é 6.5kg
        resultado = AlimentacaoService.analisar_consumo(semana_atual=1, consumo_real_kg=6.5, aves_vivas=1000)
        assert resultado["status"] == "Adequado"
        assert resultado["mensagem_alerta"] is None