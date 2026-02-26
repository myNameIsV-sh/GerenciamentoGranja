class GalpaoService:
    def __init__(self, galpao_repository):
        self.galpao_repository = galpao_repository

    def obter_galpao_por_id(self, id_galpao: int):
        galpao = self.galpao_repository.get_by_id(id_galpao)
        if not galpao:
            raise ValueError(f"Galpão com ID {id_galpao} não foi encontrado.")
        return galpao