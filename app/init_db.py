import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.logging_service import setup_logger

from app.models.Galpao import Galpao
from app.models.Lote import Lote

logger = setup_logger("init_db")

app = create_app()

def inicializar_banco():
    with app.app_context():
        try:
            logger.info("Iniciando a criação das tabelas...")
            # O create_all olha para a Base que Galpao e Lote herdaram
            db.create_all()
            logger.info("Tabelas 'galpao' e 'lote' criadas com sucesso no banco de dados!")
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {str(e)}")

if __name__ == '__main__':
    inicializar_banco()