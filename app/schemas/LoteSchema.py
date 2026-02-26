from marshmallow import fields, validate

class LoteSchema(Schema):
    id_lote = fields.Int(dump_only=True)
    id_galpao = fields.Int(required=True)
    data_alojamento = fields.Date(required=True) # ISO8601 por padrão (YYYY-MM-DD)
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