from flask_restful import Resource, reqparse
from flask import request
from repositories.favorite_repository import FavoriteRepository
from utils.auth import validate_token

UNAUTHORIZED_NO_TOKEN = "Unauthorized access token not found"
UNAUTHORIZED_INVALID_TOKEN = "Unauthorized invalid token"


class FavoritesResource(Resource):

    def __init__(self):
        self.repo = FavoriteRepository('db.json')

    def _authorize(self):
        token = request.headers.get('Authorization')

        if not token:
            return {'message': UNAUTHORIZED_NO_TOKEN}, 401

        if not validate_token(token):
            return {'message': UNAUTHORIZED_INVALID_TOKEN}, 401

        return None

    def get(self):
        auth_error = self._authorize()
        if auth_error:
            return auth_error

        return self.repo.all(), 200

    def post(self):
        auth_error = self._authorize()
        if auth_error:
            return auth_error

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')
        args = parser.parse_args()

        try:
            new_fav = self.repo.add(args['user_id'], args['product_id'])
        except ValueError as ve:
            return {'message': str(ve)}, 400
        except Exception as e:
            return {'message': 'Could not add favorite', 'detail': str(e)}, 500

        return {'message': 'Product added to favorites', 'favorite': new_fav}, 201

    def delete(self):
        auth_error = self._authorize()
        if auth_error:
            return auth_error

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')
        args = parser.parse_args()

        removed = self.repo.remove(args['user_id'], args['product_id'])
        if not removed:
            return {'message': 'Favorite not found'}, 404

        return {'message': 'Product removed from favorites'}, 200
