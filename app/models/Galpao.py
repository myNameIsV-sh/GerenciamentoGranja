from . import db

class Galpao(db.Model):
    __tablename__ = "galpao"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)

    aves = db.relationship("Ave", back_populates="galpao", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Galpao {self.nome} (Capacidade: {self.capacidade})>"