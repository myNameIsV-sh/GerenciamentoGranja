from flask_restful import Resource

class ResourceExample(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass