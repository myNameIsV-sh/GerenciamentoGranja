from . import db
from datetime import datetime

class Ave(db.Model):
    __tablename__ = "ave"

    id = db.Column(db.Integer, primary_key=True)
    data_chegada = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    galpao_id = db.Column(db.Integer, db.ForeignKey("galpao.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="VIVO") 
    data_saida = db.Column(db.Date, nullable=True)
    motivo_saida = db.Column(db.String(100), nullable=True)

    galpao = db.relationship("Galpao", back_populates="aves")

    def __repr__(self):
        return f"<Ave {self.id} - Status: {self.status}>"