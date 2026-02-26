from app.services.FotoPeriodoService import FotoPeriodoService

class TestFotoPeriodoService:

    def test_semanas_iniciais_luz_artificial(self):
        # Semana 3: Liga às 17:15 e desliga às 06:15
        resultado = FotoPeriodoService.obter_configuracao_semanal(3)
        assert resultado["horario_religamento_luzes"] == "17:15"
        assert resultado["horario_desligamento_luzes"] == "06:15"