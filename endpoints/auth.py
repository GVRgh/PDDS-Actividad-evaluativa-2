from flask import request
from flask_restful import Resource
from utils.auth import VALID_TOKEN

class AuthenticationResource(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if username == 'student' and password == 'desingp':
            token = VALID_TOKEN
            return {'token': token}, 200
        else:
            return {'message': 'unauthorized'}, 401

