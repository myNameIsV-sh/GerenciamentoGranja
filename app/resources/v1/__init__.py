from flask import Blueprint
from flask_restful import Api
from .resource_example import ResourceExample

v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1_bp)

api.add_resource(ResourceExample, '/example')