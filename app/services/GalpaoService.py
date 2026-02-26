class GalpaoService:
    def __init__(self, galpao_repository):
        self.galpao_repository = galpao_repository

    def obter_galpao_por_id(self, id_galpao: int):
        galpao = self.galpao_repository.get_by_id(id_galpao)
        if not galpao:
            raise ValueError(f"Galpão com ID {id_galpao} não foi encontrado.")
        return galpao

    def atualizar_status_ocupacao(self, id_galpao: int, novo_status: str):
        """
        Altera o status do galpão (Ex: 'Livre', 'Ocupado', 'Em Manutenção').
        """
        galpao = self.obter_galpao_por_id(id_galpao)

        # Opcional: Validar se o status é permitido
        status_permitidos = ["Livre", "Ocupado", "Em Manutenção"]
        if novo_status not in status_permitidos:
            raise ValueError(f"Status inválido. Escolha entre: {', '.join(status_permitidos)}")

        galpao.status = novo_status
        self.galpao_repository.save(galpao)
        return galpao

    def registrar_temperatura_atual(self, id_galpao: int, temperatura: float):
        """
        Caso a sua granja tenha sensores no futuro, este método
        atualiza a temperatura em tempo real.
        """
        galpao = self.obter_galpao_por_id(id_galpao)
        galpao.temperatura_atual = temperatura
        self.galpao_repository.save(galpao)

        # Pode adicionar lógica de alerta se a temperatura passar dos 30ºC, por exemplo.
        if temperatura > 30.0:
            return {"status": "Alerta", "mensagem": "Temperatura crítica! Ligar exaustores."}

        return {"status": "Normal", "mensagem": "Temperatura dentro do padrão."}