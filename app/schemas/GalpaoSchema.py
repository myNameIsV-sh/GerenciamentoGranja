from marshmallow import Schema, fields, validate

class GalpaoSchema(Schema):
    id_galpao = fields.Int(dump_only=True)
    identificacao = fields.Str(required=True, validate=validate.Length(min=1))

    status = fields.Str(validate=validate.OneOf(["Livre", "Ocupado", "Em Manutenção"]))
    temperatura_atual = fields.Int(allow_none=True)

    horario_religamento_luzes = fields.Time(format="%H:%M", allow_none=True)
    horario_desligamento_luzes = fields.Time(format="%H:%M", allow_none=True)