from app import create_app, db, setup_logger
from app.models.Galpao import Galpao
from app.models.Lote import Lote
from app.services import logging_service

logger = setup_logger()

app = create_app()

def inicializar_banco():
    with app.app_context():
        db.create_all()
        logger("Tabelas 'galpao' e 'lote' criadas com sucesso no banco de dados!")

if __name__ == '__main__':
    inicializar_banco()