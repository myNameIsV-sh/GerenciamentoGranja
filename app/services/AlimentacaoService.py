class AlimentacaoService:
    """
    Existe um rápido aumento na quantidade de comida que os animais ingerem,
    após a maturidade os ganhos são mínimos, chegando um platô.
    """
    CURVA_ALIMENTACAO = {
        1: {"racao_kg": 6.5, "fase": "Adaptação", "observacao": "Início do trato"},
        2: {"racao_kg": 10.0, "fase": "Adaptação", "observacao": "Expansão ruminal"},
        3: {"racao_kg": 14.5, "fase": "Adaptação", "observacao": "Aceleração máxima"},
        4: {"racao_kg": 18.0, "fase": "Crescimento I", "observacao": "Consolidação"},
        5: {"racao_kg": 21.0, "fase": "Crescimento I", "observacao": "Crescimento linear"},
        6: {"racao_kg": 24.0, "fase": "Crescimento I", "observacao": "Crescimento linear"},
        7: {"racao_kg": 26.0, "fase": "Crescimento II", "observacao": "Início da desaceleração"},
        8: {"racao_kg": 28.0, "fase": "Crescimento II", "observacao": "Ganho de carcaça"},
        9: {"racao_kg": 30.5, "fase": "Crescimento II", "observacao": "Ajuste de ingestão"},
        10: {"racao_kg": 32.5, "fase": "Crescimento II", "observacao": "Estabilidade"},
        11: {"racao_kg": 35.0, "fase": "Crescimento II", "observacao": "Estabilidade"},
        12: {"racao_kg": 38.0, "fase": "Crescimento II", "observacao": "Pico de crescimento"},
        13: {"racao_kg": 38.5, "fase": "Terminação", "observacao": "Início do platô"},
        14: {"racao_kg": 40.0, "fase": "Terminação", "observacao": "Acabamento"},
        15: {"racao_kg": 42.0, "fase": "Terminação", "observacao": "Acabamento"},
        16: {"racao_kg": 43.5, "fase": "Terminação", "observacao": "Capacidade máxima"},
        17: {"racao_kg": 44.5, "fase": "Terminação", "observacao": "Refino de consumo"},
        18: {"racao_kg": 45.5, "fase": "Terminação", "observacao": "Estabilização final"}
    }

    @classmethod
    def obter_meta_semanal(cls, semana_atual: int) -> dict:
        """
        Retorna a meta de consumo para a semana.
        Se passar da semana 18, o sistema entende que atingiu o platô e mantém os 45.5kg.
        """
        # Garante que a semana não seja menor que 1 e trava no máximo de 18 (o platô)
        semana_ajustada = min(max(1, semana_atual), 18)
        return cls.CURVA_ALIMENTACAO[semana_ajustada]