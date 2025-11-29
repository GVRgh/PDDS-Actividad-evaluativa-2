from flask import request
from flask_restful import Resource, reqparse
from repositories.category_repository import CategoryRepository
from utils.auth import validate_token

UNAUTHORIZED_NO_TOKEN = "Unauthorized access token not found"
UNAUTHORIZED_INVALID_TOKEN = "Unauthorized invalid token"

class CategoriesResource(Resource):
    def __init__(self):
        self.repo = CategoryRepository()

    def get(self, category_id=None):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': UNAUTHORIZED_NO_TOKEN}, 401
        if not validate_token(token):
           return { 'message': UNAUTHORIZED_INVALID_TOKEN}, 401

        if category_id:
            category = self.repo.get_by_id(category_id)
            if not category:
                return {'message': 'Category not found'}, 404
            return category, 200
         
        return self.repo.get_all(), 200 

    def post(self):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': UNAUTHORIZED_NO_TOKEN}, 401
        if not validate_token(token):
           return { 'message': UNAUTHORIZED_INVALID_TOKEN}, 401
    
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()
 
        try:
            category = self.repo.add(args['name'])
        except ValueError as e:
            return {'message': str(e)}, 400

        return {
            'message': 'Category added successfully',
            'category': category
        }, 201

    def delete(self):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': UNAUTHORIZED_NO_TOKEN}, 401
        if not validate_token(token):
           return { 'message': UNAUTHORIZED_INVALID_TOKEN}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        removed = self.repo.remove_by_name(args['name'])
        if not removed:
            return {'message': 'Category not found'}, 404

        return {'message': 'Category removed successfully'}, 200

