from flask_restful import Resource, reqparse
from flask import request
from repositories.favorite_repository import FavoriteRepository
from utils.auth import validate_token

class FavoritesResource(Resource):
    def __init__(self):
        self.repo = FavoriteRepository('db.json')

    def get(self):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Unauthorized access token not found'}, 401
        if not validate_token(token):
            return {'message': 'Unauthorized invalid token'}, 401

        return self.repo.all(), 200

    def post(self):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Unauthorized access token not found'}, 401
        if not validate_token(token):
            return {'message': 'Unauthorized invalid token'}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')
        args = parser.parse_args()

        user_id = args['user_id']
        product_id = args['product_id']

        try:
            new_fav = self.repo.add(user_id, product_id)
        except ValueError as ve:
            return {'message': str(ve)}, 400
        except Exception as e:
            return {'message': 'Could not add favorite', 'detail': str(e)}, 500

        return {'message': 'Product added to favorites', 'favorite': new_fav}, 201

    def delete(self):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Unauthorized access token not found'}, 401
        if not validate_token(token):
            return {'message': 'Unauthorized invalid token'}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')
        args = parser.parse_args()

        user_id = args['user_id']
        product_id = args['product_id']

        removed = self.repo.remove(user_id, product_id)
        if not removed:
            return {'message': 'Favorite not found'}, 404

        return {'message': 'Product removed from favorites'}, 200
