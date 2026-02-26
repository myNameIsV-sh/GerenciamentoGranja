from datetime import time

class FotoPeriodoService:
    """
        Serviço que traduz a tabela real de manejo de luz da granja.
        Valores no formato: (hora_ligar, hora_desligar).
        O valor 'None' representa os '-' ou '=' da tabela (manejo por luz natural/manual).
    """
    PROGRAMA_LUZ = {
        1: (None, time(18, 45)),
        2: (None, time(19, 30)),
        3: (time(17, 15), time(6, 15)),
        4: (time(17, 15), time(6, 15)),
        5: (time(17, 15), time(6, 15)),
        6: (time(17, 15), time(6, 15)),
        7: (time(17, 15), time(6, 15)),
        # Da semana 8 a 16 o desligamento é natural (-)
        8: (time(17, 15), None),
        9: (time(17, 15), None),
        10: (time(17, 15), None),
        11: (time(17, 15), None),
        12: (time(17, 15), None),
        13: (time(17, 15), None),
        14: (time(17, 15), None),
        15: (time(17, 15), None),
        16: (time(17, 15), None),
        # Retoma o padrão até o fim do lote
        17: (time(17, 15), time(6, 15)),
        18: (time(17, 15), time(6, 15)),
        19: (time(17, 15), time(6, 15)),
        20: (time(17, 15), time(6, 15)),
        21: (time(17, 15), time(6, 15)),
        22: (time(17, 15), time(6, 15)),
        23: (time(17, 15), time(6, 15)),
        24: (time(17, 15), time(6, 15)),
        25: (time(17, 15), time(6, 15))
    }

    @classmethod
    def obter_configuracao_semanal(cls, semana_atual: int) -> dict:
        """Busca os horários e retorna formatado para o GalpaoService"""
        # Trava na semana 25. Se a ave tiver 30 semanas, mantém o manejo da semana 25.
        semana_ajustada = min(max(1, semana_atual), 25)
        acionamento, desligamento = cls.PROGRAMA_LUZ[semana_ajustada]

        # Formata para string HH:MM ou retorna nulo se for acompanhamento natural
        hora_ligar_str = acionamento.strftime("%H:%M") if acionamento else None
        hora_desligar_str = desligamento.strftime("%H:%M") if desligamento else None

        return {
            "semana_atual": semana_ajustada,
            "horario_religamento_luzes": hora_ligar_str,
            "horario_desligamento_luzes": hora_desligar_str,
            "orientacao_manejo": cls._obter_observacao(semana_ajustada)
        }

    @classmethod
    def _obter_observacao(cls, semana: int) -> str:
        if semana <= 2:
            return "As luzes permanecem acesas durante todo o dia, sendo apagadas apenas no período noturno."
        elif 3 <= semana <= 7:
            return "Em dias com baixa iluminação natural (nublados/chuvosos), as luzes devem ser ligadas também durante o dia."
        elif semana == 16:
            return "Atenção: Fator de Ajuste (Manejo crítico de fase)."
        return "Programa de luz padrão."
