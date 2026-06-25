from marshmallow import Schema, fields, validate, post_load
from app.models.Lote import Lote

class LoteBaseSchema(Schema):
    id_lote = fields.Int()
    id_galpao = fields.Int(required=True)
    data_alojamento = fields.Date(required=True)
    status = fields.Str(validate=validate.OneOf(["Ativo", "Finalizado"]))
    quantidade_inicial_aves = fields.Int(required=True, validate=validate.Range(min=1))
    ultimo_peso_g = fields.Float(validate=validate.Range(min=0))
    consumo_total_racao_kg = fields.Float(validate=validate.Range(min=0))
    mortalidade_acumulada = fields.Int(validate=validate.Range(min=0))

    @post_load
    def make_lote(self, data, **kwargs):
        return Lote(**data)

class LoteReadSchema(LoteBaseSchema):
    semana_atual = fields.Method("get_semana_atual", dump_only=True)

    def get_semana_atual(self, obj):
        return obj.calcular_idade_em_semanas

class RegistroConsumoSchema(Schema):
    racao_consumida_kg = fields.Float(
        required=True,
        validate=validate.Range(min=0.1, error="A quantidade de ração deve ser maior que zero.")
    )