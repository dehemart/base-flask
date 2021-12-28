from flask import abort, jsonify, make_response, request
from flask_restful import Resource

from base.models.product import Product
from base.extensions.database import db


class ProductResource(Resource):
    """" API Resource of User """

    def get(self, id: int = None):
        if id:
            return self._get_one(id)
        else:
            return self._get_all()

    def _get_all(self):
        product = Product.query.all() or abort(400, "Products not found")
        response_data = jsonify(
            {"products": [product.to_dict() for product in product]})
        return make_response(response_data, 200)

    def _get_one(self, id: int = None):
        product = Product.query.filter_by(
            id=id).first() or abort(400, "Product not found")
        response_data = jsonify({"product": product.to_dict()})
        return make_response(response_data, 200)

    def put(self, id: int = None):
        product_data = request.get_json()

        if id:
            product = Product.query.filter_by(id=id).first()
        else:
            product = None
        try:
            if product:
                response_code = 200
                product.sku = product_data["sku"].upper(
                ) if product_data["sku"] is None else product.sku.upper()
                product.name = product_data["name"] if product_data["name"] is None else product.name
                product.description = product_data["description"] if product_data[
                    "description"] is None else product.description
                product.status_id = product_data["status_id"] if product_data["status_id"] is None else product.status_id
                product.category_id = product_data["category_id"] if product_data[
                    "category_id"] is None else product.category_id
            else:
                response_code = 201
                product = Product(
                    product_data["sku"].upper(),
                    product_data["name"],
                    product_data["description"],
                    product_data["status_id"],
                    product_data["category_id"]
                )

            db.session.add(product)
            db.session.commit()
        except ValueError as ve:
            abort(400, "Bad Request: " + ve.__str__())

        response_data = jsonify({"product": product.to_dict()})
        return make_response(response_data, response_code)

    def post(self):
        product_data = request.get_json()

        product_validation = Product.query.filter_by(
            sku=product_data["sku"]).first()

        if product_validation:
            abort(422, "Product with sku duplicated")
        try:
            product = Product(
                sku=product_data["sku"].upper(),
                name=product_data["name"],
                description=product_data["description"],
                status_id=product_data["status_id"],
                category_id=product_data["category_id"]
            )

            db.session.add(product)
            db.session.commit()
        except ValueError as ve:
            abort(400, "Bad Request: " + ve.__str__())

        response_data = jsonify({"product": product.to_dict()})

        return make_response(response_data, 201)

    def delete(self, id: int = None):
        product = Product.query.filter_by(id=id).first() or abort(404)
        if product:
            db.session.delete(product)
            db.session.commit()

        return make_response("User was deleted", 200)
