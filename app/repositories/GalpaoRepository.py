from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.Galpao import Galpao

class GalpaoRepository:
    def get_by_id(self, id_galpao: int):
        """Busca o galpão pelo ID."""
        return db.session.get(Galpao, id_galpao)

    def save(self, galpao: Galpao):
        """Persiste as alterações (luzes, temperatura, status)."""
        db.session.add(galpao)
        db.session.commit()
        return galpao

    def listar_todos(self):
        """Útil para o dashboard mostrar todos os galpões."""
        return db.session.query(Galpao).all()