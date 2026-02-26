import os
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from sqlalchemy import text
from app.database import db, ma
from app.services.logging_service import setup_logger

logger = setup_logger()

load_dotenv()

api = Api()

def test_db_connection():
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("Conexão OK")
    except Exception as e:
        logger.error("Erro na conexão:", e)

def create_app():
    app = Flask(__name__)

    # Importação local para evitar recursão
    from app.resources.v1 import v1_bp

    app.register_blueprint(v1_bp)

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)

    from app.models import Galpao, Lote

    with app.app_context():
        test_db_connection() 

    logger.info("Aplicação Flask iniciada com Flask-RESTful")

    

    return app
