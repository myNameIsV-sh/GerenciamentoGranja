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