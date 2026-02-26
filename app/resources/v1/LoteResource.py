from flask import request
from flask_restful import Resource
from app.schemas.LoteSchema import LoteSchema
from app.services.logging_service import setup_logger

logger = setup_logger("LoteResource")

class LoteResource(Resource):
    def __init__(self, **kwargs):
        # O Service será injetado pelo app.py
        self.lote_service = kwargs.get('lote_service')
        self.lote_schema = LoteSchema()
        self.lotes_schema = LoteSchema(many=True)

    def get(self, id_lote=None):
        """READ: Busca um lote específico ou lista todos."""
        try:
            if id_lote:
                lote = self.lote_service.obter_lote(id_lote)
                if not lote:
                    return {"message": "Lote não encontrado."}, 404
                return self.lote_schema.dump(lote), 200

            # Se não passar ID, lista todos
            lotes = self.lote_service.listar_todos()
            return self.lotes_schema.dump(lotes), 200
        except Exception as e:
            logger.error(f"Erro ao buscar lote(s): {str(e)}")
            return {"message": "Erro interno no servidor."}, 500

    def post(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass