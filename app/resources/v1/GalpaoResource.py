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
        data = request.get_json() or {}
        errors = self.galpao_schema.validate(data)
        if errors:
            return {"erros": errors}, 400

        try:
            novo_galpao = self.galpao_service.criar_galpao(data)
            return self.galpao_schema.dump(novo_galpao), 201
        except Exception as e:
            return {"message": str(e)}, 400

    def put(self, id_galpao=None):
        """UPDATE: Atualiza status ('Ocupado'/'Livre') ou temperatura."""
        if not id_galpao:
            return {"message": "Rota inválida. O ID do galpão é obrigatório no URL."}, 400

        data = request.get_json() or {}

        try:
            # Se for uma requisição específica de sensor de temperatura
            if 'temperatura_atual' in data:
                resultado = self.galpao_service.registrar_temperatura_atual(
                    id_galpao, data['temperatura_atual']
                )
                return resultado, 200

            # Se for uma requisição de status de ocupação
            if 'status' in data:
                galpao = self.galpao_service.atualizar_status_ocupacao(id_galpao, data['status'])
                return self.galpao_schema.dump(galpao), 200

            # Atualização genérica de outros campos
            galpao_atualizado = self.galpao_service.atualizar_galpao(id_galpao, data)
            return self.galpao_schema.dump(galpao_atualizado), 200

        except ValueError as e:
            return {"message": str(e)}, 400  # Bad Request para validações de negócio
        except Exception as e:
            return {"message": "Erro interno ao atualizar galpão."}, 500

    def delete(self, id_galpao):
        """DELETE: Remove o galpão do banco de dados."""
        if not id_galpao:
            return {"message": "ID do galpão é obrigatório."}, 400

        try:
            sucesso = self.galpao_service.deletar_galpao(id_galpao)
            if sucesso:
                return {"message": "Galpão deletado com sucesso."}, 204
            return {"message": "Galpão não encontrado."}, 404
        # É importante capturar erros de banco de dados aqui (ex: Galpão ainda tem Lotes)
        except Exception as e:
            logger.error(f"Tentativa de deletar galpão falhou: {str(e)}")
            return {
                "message": "Não foi possível deletar o galpão. Verifique se existem lotes ativos vinculados a ele."}, 409  # 409 Conflict