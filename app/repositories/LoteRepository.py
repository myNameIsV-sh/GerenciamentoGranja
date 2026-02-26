from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.Lote import Lote

class LoteRepository:
    def get_lote(self, id_lote: int):
        """Busca um lote pelo ID. Se não encontrar, retorna None."""
        return db.session.get(Lote, id_lote)

    def save(self, lote: Lote):
        """Salva ou atualiza um lote no banco de dados."""
        db.session.add(lote)
        db.session.commit()
        return lote

    def delete(self, lote: Lote):
        """Remove um lote (útil para encerramento de ciclos)."""
        db.session.delete(lote)
        db.session.commit()