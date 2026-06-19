from flask import request
from flask_restful import Resource
from app.schemas.LoteSchema import LoteBaseSchema, LoteReadSchema, RegistroConsumoSchema
from app.services.logging_service import setup_logger

logger = setup_logger("LoteResource")

class LoteResource(Resource):
    def __init__(self, **kwargs):
        # O Service será injetado pelo app.py
        self.lote_service = kwargs.get('lote_service')
        self.lote_schema = LoteBaseSchema() # Para POST/PUT
        self.lote_read_schema = LoteReadSchema() # Para GET
        self.lotes_read_schema = LoteReadSchema(many=True) # Para GET list

    def get(self, id_lote=None):
        """READ: Busca um lote específico ou lista todos."""
        try:
            if id_lote:
                lote = self.lote_service.obter_lote(id_lote)
                if not lote:
                    return {"message": "Lote não encontrado."}, 404
                return self.lote_read_schema.dump(lote), 200

            # Se não passar ID, lista todos
            lotes = self.lote_service.listar_todos()
            return self.lotes_read_schema.dump(lotes), 200
        except Exception as e:
            logger.error(f"Erro ao buscar lote(s): {str(e)}")
            return {"message": "Erro interno no servidor."}, 500

    def post(self):
        """CREATE: Aloja um novo lote na granja."""
        # Usa 'or {}' para evitar erro se o cliente esquecer o Content-Type: application/json
        data = request.get_json() or {}

        errors = self.lote_schema.validate(data)
        if errors:
            logger.warning(f"Tentativa de criar lote com dados inválidos: {errors}")
            return {"erros": errors}, 400

        # 2. Execução
        try:
            novo_lote = self.lote_service.criar_lote(data)
            logger.info(f"Novo lote alojado com sucesso: ID {novo_lote.id_lote}")
            return self.lote_schema.dump(novo_lote), 201
        except Exception as e:
            logger.error(f"Erro ao criar lote: {str(e)}")
            return {"message": str(e)}, 400

    def put(self, id_lote=None):
        """UPDATE: Atualiza dados do lote OU registra o consumo semanal."""
        if not id_lote:
            return {"message": "Rota inválida. O ID do lote é obrigatório no URL para atualização."}, 400

        data = request.get_json() or {}

        # Verifica se é a requisição especial de consumo de ração
        if 'racao_consumida_kg' in data:
            consumo_schema = RegistroConsumoSchema()
            errors = consumo_schema.validate(data)
            if errors:
                return {"erros": errors}, 400

            try:
                # Chama a inteligência de negócio que criamos!
                resultado = self.lote_service.registrar_consumo_semanal(
                    id_lote=id_lote,
                    racao_consumida_kg=data['racao_consumida_kg']
                )
                return resultado, 200
            except ValueError as e:
                return {"message": str(e)}, 404
            except Exception as e:
                return {"message": "Erro ao registrar consumo."}, 500

        # Caso seja uma atualização comum (ex: atualizar o status)
        try:
            lote_atualizado = self.lote_service.atualizar_lote(id_lote, data)
            if not lote_atualizado:
                return {"message": "Lote não encontrado."}, 404
            return self.lote_schema.dump(lote_atualizado), 200
        except Exception as e:
            return {"message": str(e)}, 400

    def delete(self, id_lote=None):
        """DELETE: Remove o lote do sistema."""
        if not id_lote:
            return {"message": "Rota inválida. O ID do lote é obrigatório no URL para exclusão."}, 400

        try:
            sucesso = self.lote_service.deletar_lote(id_lote)
            if sucesso:
                return {"message": "Lote deletado com sucesso."}, 204  # 204 = No Content (Padrão REST)
            return {"message": "Lote não encontrado."}, 404
        except Exception as e:
            return {"message": str(e)}, 500