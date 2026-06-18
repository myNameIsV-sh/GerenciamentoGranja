from marshmallow import Schema, fields, validate, post_load
from app.models.Lote import Lote

class LoteSchema(Schema):
    id_lote = fields.Int()
    id_galpao = fields.Int(required=True)
    data_alojamento = fields.Date(required=True)  # ISO8601 por padrão (YYYY-MM-DD)
    status = fields.Str(validate=validate.OneOf(["Ativo", "Finalizado"]))

    quantidade_inicial_aves = fields.Int(required=True, validate=validate.Range(min=1))
    ultimo_peso_g = fields.Float(validate=validate.Range(min=0))
    consumo_total_racao_kg = fields.Float(validate=validate.Range(min=0))
    mortalidade_acumulada = fields.Int(validate=validate.Range(min=0))

    # Campo calculado para expor a idade em semanas no JSON
    semana_atual = fields.Method("get_semana_atual", dump_only=True)

    def get_semana_atual(self, obj):
        # Chama a property definida na classe Lote
        return obj.calcular_idade_em_semanas

    @post_load
    def make_lote(self, data, **kwargs):
        return Lote(**data)


# <-- NOVO: O Schema específico para a rota de consumo que havíamos planejado
class RegistroConsumoSchema(Schema):
    racao_consumida_kg = fields.Float(
        required=True,
        validate=validate.Range(min=0.1, error="A quantidade de ração deve ser maior que zero.")
    )