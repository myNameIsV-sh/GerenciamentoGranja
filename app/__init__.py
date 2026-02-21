from flask import Flask
from app.services.logging_service import setup_logger

logger = setup_logger()

def create_app():
    app = Flask(__name__)

    # Importação local para evitar recursão
    from app.resources.v1 import v1_bp

    app.register_blueprint(v1_bp)

    logger.info("Aplicação Flask iniciada com Flask-RESTful")

    return app