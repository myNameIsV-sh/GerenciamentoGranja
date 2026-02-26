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
            db.session.add(galpao)
            db.session.commit()
            logger.info(f"Galpão {galpao.id_galpao} ({galpao.identificacao}) atualizado com sucesso.")
            return galpao
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.critical(f"Erro fatal ao salvar galpão {galpao.id_galpao}: {str(e)}")
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
            id_removido = galpao.id_galpao
            db.session.delete(galpao)
            db.session.commit()
            logger.info(f"Galpão {id_removido} removido do sistema.")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao deletar galpão: {str(e)}")
            return False