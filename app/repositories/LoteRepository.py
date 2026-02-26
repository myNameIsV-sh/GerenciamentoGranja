from app.database import db
from app.models.Lote import Lote
from sqlalchemy.exc import SQLAlchemyError
from app.services.logging_service import setup_logger

logger = setup_logger("LoteRepository")

class LoteRepository:
    def get_lote(self, id_lote: int):
        """Busca um lote pelo ID com logging de erro."""
        try:
            lote = db.session.get(Lote, id_lote)
            if not lote:
                logger.warning(f"Lote {id_lote} não encontrado no banco.")
            return lote
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar lote {id_lote}: {str(e)}")
            return None

    def listar_todos(self):
        """Lista todos os lotes cadastrados."""
        try:
            lotes = db.session.query(Lote).all()
            logger.debug(f"Listagem de lotes executada. Total: {len(lotes)}")
            return lotes
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar lotes: {str(e)}")
            return []

    def save(self, lote: Lote):
        """Salva o lote e registra o sucesso ou falha crítica."""
        try:
            db.session.add(lote)
            db.session.commit()
            logger.info(f"Lote {lote.id_lote} atualizado com sucesso (Consumo Acumulado: {lote.consumo_total_racao_kg}kg).")
            return lote
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.critical(f"Falha ao salvar lote {lote.id_lote}: {str(e)}")
            raise e

    def delete(self, lote: Lote):
        """Remove o lote e loga a exclusão."""
        try:
            id_removido = lote.id_lote
            db.session.delete(lote)
            db.session.commit()
            logger.info(f"Lote {id_removido} removido do sistema.")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao deletar lote: {str(e)}")
            return False