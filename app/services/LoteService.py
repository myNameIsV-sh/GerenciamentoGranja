from app.services.AlimentacaoService import AlimentacaoService
from app.services.FotoPeriodoService import FotoPeriodoService

class LoteService:
    # Injeção do galpao_service em vez do galpao_repository
    def __init__(self, lote_repository, galpao_service):
        self.lote_repository = lote_repository
        self.galpao_service = galpao_service

    def registrar_consumo_semanal(self, id_lote: int, racao_consumida_kg: float):
        # 1. Busca o lote no banco de dados (via Repository)
        lote = self.lote_repository.get_lote(id_lote)

        # 2. Descobre qual é a semana atual dinamicamente
        semana_atual = lote.calcular_idade_em_semanas

        aves_vivas = lote.quantidade_inicial_aves - lote.mortalidade_acumulada

        # 3. Passa os dados para o AlimentacaoService validar as regras
        analise_alimentacao = AlimentacaoService.analisar_consumo(semana_atual, racao_consumida_kg, aves_vivas)

        config_luz = FotoPeriodoService.obter_configuracao_semanal(semana_atual)

        self.galpao_service.atualizar_configuracao_luz(lote.id_galpao, config_luz)

        # 4. Atualiza o model com o total acumulado
        lote.consumo_total_racao_kg += racao_consumida_kg
        self.lote_repository.save(lote)

        # 5. Se houver alerta, podemos retornar isso para o Frontend exibir um aviso vermelho!
        return {
            "analise_alimentacao": analise_alimentacao,
            "configuracao_luz_aplicada": config_luz
        }

    def obter_lote(self, id_lote: int):
        """Busca um lote específico no banco."""
        return self.lote_repository.get_lote(id_lote)

    def listar_todos(self):
        """Lista todos os lotes cadastrados."""
        return self.lote_repository.listar_todos()

    def criar_lote(self, dados: dict):
        """Cria uma nova instância de Lote e salva no banco."""
        from app.models.Lote import Lote
        novo_lote = Lote(**dados)
        return self.lote_repository.save(novo_lote)

    def atualizar_lote(self, id_lote: int, dados: dict):
        """Atualiza dinamicamente os campos permitidos de um lote."""
        lote = self.obter_lote(id_lote)
        if not lote:
            return None

        # Atualiza os atributos do objeto iterando sobre o dicionário
        for key, value in dados.items():
            if hasattr(lote, key) and key != 'id_lote':  # Evita mudar a Primary Key
                setattr(lote, key, value)

        return self.lote_repository.save(lote)

    def deletar_lote(self, id_lote: int):
        """Remove o lote do banco de dados."""
        lote = self.obter_lote(id_lote)
        if not lote:
            return False
        return self.lote_repository.delete(lote)