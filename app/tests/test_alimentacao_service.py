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
        
        
    def test_consumo_abaixo(self):
        # Semana 1 (1000 aves): Limite inferior é 6.5 * 0.9 = 5.85kg
        resultado = AlimentacaoService.analisar_consumo(1, 5.0, 1000)
        assert resultado["status"] == "Abaixo do Esperado"
        assert "Atenção: Consumo de 5.0kg está abaixo do limite" in resultado["mensagem_alerta"]
        
        
    def test_consumo_acima(self):
        # Semana 1 (1000 aves): Limite superior é 6.5 * 1.1 = 7.15kg
        resultado = AlimentacaoService.analisar_consumo(1, 8.0, 1000)
        assert resultado["status"] == "Acima do Esperado"
        assert "excede o limite" in resultado["mensagem_alerta"]
        
        
    def test_proporcao_lote(self):
        # Semana 1: meta base 6.5kg. Para 5000 aves, esperado é 6.5 * 5 = 32.5kg
        resultado = AlimentacaoService.analisar_consumo(1, 32.5, 5000)
        assert resultado["meta_esperada_lote_kg"] == 32.5
        assert resultado["status"] == "Adequado"