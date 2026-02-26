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

    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass