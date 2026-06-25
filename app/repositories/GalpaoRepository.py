from app.database import db
from app.models.Galpao import Galpao
from sqlalchemy.exc import SQLAlchemyError
from app.services.logging_service import setup_logger

logger = setup_logger("GalpaoRepository")

class GalpaoRepository:
    def get_by_id(self, id_galpao: int):
        try:
            return db.session.get(Galpao, id_galpao)
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar galpão {id_galpao}: {str(e)}")
            return None

    def save(self, galpao: Galpao):
        try:
            # Usar merge em vez de add para garantir que instâncias vindas 
            # de fora da sessão (cache) sejam atualizadas corretamente
            galpao_persisted = db.session.merge(galpao)
            db.session.commit()
            logger.info(f"Galpão {galpao_persisted.id_galpao} ({galpao_persisted.identificacao}) atualizado com sucesso.")
            return galpao_persisted
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.critical(f"Erro fatal ao salvar galpão: {str(e)}")
            raise e

    def listar_todos(self):
        try:
            galpoes = db.session.query(Galpao).all()
            logger.debug(f"Listagem de galpões executada. Total: {len(galpoes)}")
            return galpoes
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar galpões: {str(e)}")
            return []

    def delete(self, galpao: Galpao):
        """Remove o galpão e loga a exclusão."""
        try:
            # Garante que o objeto está na sessão atual do banco de dados
            if galpao not in db.session:
                galpao = db.session.merge(galpao)
            
            id_removido = galpao.id_galpao
            db.session.delete(galpao)
            db.session.commit()
            logger.info(f"Galpão {id_removido} removido do sistema.")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao deletar galpão: {str(e)}")
            return False