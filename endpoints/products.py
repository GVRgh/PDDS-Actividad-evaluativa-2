from flask_restful import Resource, reqparse
from flask import request
from repositories.product_repository import ProductRepository
from utils.auth import validate_token

UNAUTHORIZED_NO_TOKEN = "Unauthorized access token not found"
UNAUTHORIZED_INVALID_TOKEN = "Unauthorized invalid token"

class ProductsResource(Resource):
    def __init__(self):

        self.repo = ProductRepository('db.json')

        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('name', type=str, required=True, help='Name of the product')
        self.post_parser.add_argument('category', type=str, required=True, help='Category of the product')
        self.post_parser.add_argument('price', type=float, required=True, help='Price of the product')

        
    def get(self, product_id=None):
        token = request.headers.get('Authorization')
        category_filter = request.args.get('category')
      
        if not token:
            return { 'message': UNAUTHORIZED_NO_TOKEN}, 401

        if not validate_token(token):
           return { 'message': UNAUTHORIZED_INVALID_TOKEN}, 401

        if category_filter:
            filtered_products = self.repo.filter_by_category(category_filter)
            return filtered_products, 200
        
        if product_id is not None:
            product = self.repo.get_by_id(product_id)
            if product is not None:
                return product, 200
            else:
                return {'message': 'Product not found'}, 404
              
        return self.repo.all(), 200

    def post(self):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': UNAUTHORIZED_NO_TOKEN}, 401

        if not validate_token(token):
            return {'message': UNAUTHORIZED_INVALID_TOKEN}, 401
        
        args = self.post_parser.parse_args()
        product = {
            'name': args['name'],
            'category': args['category'],
            'price': args['price']
        }

        try:
            new_product = self.repo.add(product)
        except ValueError as ve:
            return {'message': str(ve)}, 400
        except Exception as e:
            # Generic error -> internal server error
            return {'message': 'Could not add product', 'detail': str(e)}, 500

        return {'message': 'Product added', 'product': new_product}, 201


