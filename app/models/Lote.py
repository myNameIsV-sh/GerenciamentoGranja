from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Date, ForeignKey
from app.database import Base
from datetime import date
from typing import TYPE_CHECKING # Importe isso

if TYPE_CHECKING:
    from .Galpao import Galpao

class Lote(Base):
    __tablename__ = "lote"

    id_lote: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_galpao: Mapped[int] = mapped_column(ForeignKey("galpao.id_galpao"), nullable=False)

    data_alojamento: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Ativo")

    quantidade_inicial_aves: Mapped[int] = mapped_column(Integer, nullable=False)

    # Métricas
    ultimo_peso_g: Mapped[float] = mapped_column(Float, default=0.0)
    consumo_total_racao_kg: Mapped[float] = mapped_column(Float, default=0.0)
    mortalidade_acumulada: Mapped[int] = mapped_column(Integer, default=0)

    # Relacionamento: O lote conhece seu galpão
    galpao: Mapped["Galpao"] = relationship("Galpao", back_populates="lotes")

    @property
    def calcular_idade_em_semanas(self) -> int:
        """Calcula a semana atual baseada na data de hoje."""
        hoje = date.today()
        diferenca = hoje - self.data_alojamento
        # +1 para garantir que o dia 0-6 seja 'Semana 1'
        return (diferenca.days // 7) + 1