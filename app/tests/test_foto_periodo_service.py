from app.services.FotoPeriodoService import FotoPeriodoService

class TestFotoPeriodoService:

    def test_semanas_iniciais_luz_artificial(self):
        # Semana 3: Liga às 17:15 e desliga às 06:15
        resultado = FotoPeriodoService.obter_configuracao_semanal(3)
        assert resultado["horario_religamento_luzes"] == "17:15"
        assert resultado["horario_desligamento_luzes"] == "06:15"
        
        
    def test_luz_natural_desligamento(self):
        # Semana 10: Desligamento é natural (None)
        resultado = FotoPeriodoService.obter_configuracao_semanal(10)
        assert resultado["horario_religamento_luzes"] == "17:15"
        assert resultado["horario_desligamento_luzes"] is None
        
    def test_teto_de_semanas(self):
        # Semana 50: Deve travar na semana 25
        resultado = FotoPeriodoService.obter_configuracao_semanal(50)
        assert resultado["semana_atual"] == 25