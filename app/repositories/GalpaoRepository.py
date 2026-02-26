from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.Galpao import Galpao

class GalpaoRepository:
    def __init__(self, db: Session):
        pass
    def save(self, galpao: Galpao):
        pass