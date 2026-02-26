from flask import request
from flask_restful import Resource
from app.schemas.GalpaoSchema import GalpaoSchema
from app.services.logging_service import setup_logger

logger = setup_logger("GalpaoResource")

class GalpaoResource(Resource):
    def __init__(self, **kwargs):
        self.galpao_service = kwargs.get('galpao_service')
        self.galpao_schema = GalpaoSchema()
        self.galpoes_schema = GalpaoSchema(many=True)

    def get(self, id_galpao=None):
        """READ: Busca um galpão ou a lista completa de infraestrutura."""
        try:
            if id_galpao:
                galpao = self.galpao_service.obter_galpao_por_id(id_galpao)
                if not galpao:
                    return {"message": "Galpão não encontrado."}, 404
                return self.galpao_schema.dump(galpao), 200

            galpoes = self.galpao_service.listar_todos()
            return self.galpoes_schema.dump(galpoes), 200
        except Exception as e:
            logger.error(f"Erro ao buscar galpão: {str(e)}")
            return {"message": "Erro interno no servidor."}, 500

    def post(self):
        """CREATE: Registra um novo galpão construído."""
        data = request.get_json()
        errors = self.galpao_schema.validate(data)
        if errors:
            return {"erros": errors}, 400

        try:
            novo_galpao = self.galpao_service.criar_galpao(data)
            return self.galpao_schema.dump(novo_galpao), 201
        except Exception as e:
            return {"message": str(e)}, 400

    def put(self):
        pass
    def delete(self):
        pass