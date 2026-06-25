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
        # TODO: Transformar esses campos em números, ex.: 0, 1, 2
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

    def atualizar_configuracao_luz(self, id_galpao: int, config_luz: dict):
        """
        Recebe a configuração do FotoPeriodoService e atualiza o galpão.
        """
        galpao = self.obter_galpao_por_id(id_galpao)

        galpao.horario_religamento_luzes = config_luz.get("horario_religamento_luzes")
        galpao.horario_desligamento_luzes = config_luz.get("horario_desligamento_luzes")

        self.galpao_repository.save(galpao)
        return galpao

    def listar_todos(self):
        """Busca todos os galpões."""
        return self.galpao_repository.listar_todos()

    def criar_galpao(self, dados: dict):
        """Instancia e salva um novo galpão."""
        from app.models.Galpao import Galpao
        novo_galpao = Galpao(**dados)
        return self.galpao_repository.save(novo_galpao)

    def atualizar_galpao(self, id_galpao: int, dados: dict):
        """Atualiza dinamicamente os dados do galpão (nome, etc)."""
        galpao = self.obter_galpao_por_id(id_galpao)

        for key, value in dados.items():
            if hasattr(galpao, key) and key != 'id_galpao':
                setattr(galpao, key, value)

        return self.galpao_repository.save(galpao)

    def deletar_galpao(self, id_galpao: int):
        """Deleta o galpão, com verificação de segurança."""
        galpao = self.obter_galpao_por_id(id_galpao)
        if not galpao:
            return False

        # Segurança: Não deixa apagar galpão que ainda tem lotes dentro
        if galpao.lotes:
            raise ValueError("Não é possível deletar um galpão que possui lotes vinculados.")

        return self.galpao_repository.delete(galpao)