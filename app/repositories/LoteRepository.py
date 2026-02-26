from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.Lote import Lote

class LoteRepository:
    def __init__(self, session: Session):
        self.session = session
    def save(self, lote: Lote):
        pass
