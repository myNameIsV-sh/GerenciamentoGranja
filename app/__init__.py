from flask import Flask
from flask_restful import Api
from logger import setup_logger  

logger = setup_logger()

def create_app():
    app = Flask(__name__)

    api = Api(app)

    logger.info("Aplicação Flask iniciada com Flask-RESTful")

    

    return app
