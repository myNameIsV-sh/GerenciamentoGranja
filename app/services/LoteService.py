from app.services import AlimentacaoService

class LoteService:
    def __init__(self, lote_repository):
        self.lote_repository = lote_repository

    def registrar_consumo_semanal(self, id_lote: int, racao_consumida_kg: float):
        # 1. Busca o lote no banco de dados (via Repository)
        lote = self.lote_repository.get_lote(id_lote)

        # 2. Descobre qual é a semana atual dinamicamente
        semana_atual = lote.calcular_idade_em_semanas

        aves_vivas = lote.quantidade_inicial_aves - lote.mortalidade_acumulada

        # 3. Passa os dados para o AlimentacaoService validar as regras
        analise = AlimentacaoService.analisar_consumo(semana_atual, racao_consumida_kg, aves_vivas)

        # 4. Atualiza o model com o total acumulado
        lote.consumo_total_racao_kg += racao_consumida_kg
        self.lote_repository.save(lote)

        # 5. Se houver alerta, podemos retornar isso para o Frontend exibir um aviso vermelho!
        return analise