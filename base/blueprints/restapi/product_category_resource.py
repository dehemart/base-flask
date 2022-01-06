from flask import abort, jsonify, make_response, request
from flask_restful import Resource

from base.extensions.database import db
from base.models.product_category import ProductCategory


class ProductCategoryResource(Resource):
    """" API Resource of product """

    def get(self, id: int = None):
        if id:
            return self._get_one(id)
        else:
            return self._get_all()  

    def _get_all(self):
        product_categoryes = ProductCategory.query.all() or abort(
            400, "Product categories not found")
        response_data = jsonify(   
            {'product_category': [product_category.to_dict() for product_category in product_categoryes]})
        return make_response(response_data, 200)

    def _get_one(self, id: int):
        product_category = ProductCategory.query.filter_by(
            id=id).first() or abort(404, "Product category not found")
        response_data = jsonify(
            {'product_category': product_category.to_dict()})
        return make_response(response_data, 200)

    def put(self, id: int = None):
        product_category_data = request.get_json()

        if id:
            product_category = ProductCategory.query.filter_by(id=id).first()
        else:
            product_category = None
        try:
            if product_category:
                return_code = 200
                product_category.name = product_category_data['name'] if product_category_data[
                    'name'] is None else product_category.name
                product_category.active = product_category_data['active'] if product_category_data[
                    'active'] is None else product_category.active
            else:
                return_code = 201
                product_category = ProductCategory(name=product_category_data['name'],
                                                   active=product_category_data['active']
                                                   )
            db.session.add(product_category)
            db.session.commit()
        except ValueError as ve:
            abort(400, "Bad Request: " + ve.__str__())
        response_data = jsonify(
            {'product_category': product_category.to_dict()}
        )
        return make_response(response_data, return_code)

    def post(self):
        product_category_data = request.get_json()

        product_category = ProductCategory.query.filter_by(
            name=product_category_data['name']).first()
        if product_category:
            abort(422, "Category duplicated")
        try:
            product_category = ProductCategory(name=product_category_data['name'],
                                               active=product_category_data['active']
                                               )

            db.session.add(product_category)
            db.session.commit()
        except ValueError as ve:
            abort(400, "Bad Request: " + ve.__str__())
        response_data = jsonify(
            {'product_category': product_category.to_dict()})

        return make_response(response_data, 201)

    def delete(self, id: int = None):
        product_category = ProductCategory.query.filter_by(
            id=id).first() or abort(404)
        if product_category:
            db.session.delete(product_category)
            db.session.commit()

        return make_response("Product category was deleted", 200)
