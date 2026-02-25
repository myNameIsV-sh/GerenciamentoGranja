from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Time
from database import Base
from datetime import time
from typing import Optional, List

class Galpao(Base):
    __tablename__ = "galpao"

    id_galpao: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    identificacao: Mapped[str] = mapped_column(String(50), nullable=False)
    temperatura_galpao: Mapped[Optional[int]] = mapped_column(Integer)

    # Configurações de iluminação
    horario_religamento_luzes: Mapped[Optional[time]] = mapped_column(Time)
    horario_desligamento_luzes: Mapped[Optional[time]] = mapped_column(Time)

    # Relacionamento: Um galpão conhece seus lotes
    lotes: Mapped[List["Lote"]] = relationship("Lote", back_populates="galpao")