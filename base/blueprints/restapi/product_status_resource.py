from flask import abort, jsonify, make_response, request
from flask_restful import Resource

from base.extensions.database import db
from base.models.product_status import ProductStatus


class ProductStatusResource(Resource):
    """" API Resource of product """

    def get(self, id: int = None):
        if id:
            return self._get_one(id)
        else:
            return self._get_all()

    def _get_all(self):
        product_statuses = ProductStatus.query.all() or abort(
            400, "Product Statuses not found")
        response_data = jsonify(
            {'product_status': [product_status.to_dict() for product_status in product_statuses]})
        return make_response(response_data, 200)

    def _get_one(self, id: int):
        product_status = ProductStatus.query.filter_by(
            id=id).first() or abort(404, "ProductStatus not found")
        response_data = jsonify({'product_status': product_status.to_dict()})
        return make_response(response_data, 200)

    def put(self, id: int = None):
        product_status_data = request.get_json()

        if id:
            product_status = ProductStatus.query.filter_by(id=id).first()
        else:
            product_status = None
        try:
            if product_status:
                return_code = 200
                product_status.name = product_status_data['name'] if product_status_data[
                    'name'] is None else product_status.name
                product_status.active = product_status_data['active'] if product_status_data[
                    'active'] is None else product_status.active
            else:
                return_code = 201
                product_status = ProductStatus(name=product_status_data['name'],
                                               active=product_status_data['active']
                                               )
            db.session.add(product_status)
            db.session.commit()
        except ValueError as ve:
            abort(400, "Bad Request: " + ve.__str__())
        response_data = jsonify(
            {'product_status': product_status.to_dict()}
        )
        return make_response(response_data, return_code)

    def post(self):
        product_status_data = request.get_json()

        product_status = ProductStatus.query.filter_by(
            name=product_status_data['name']).first()
        if product_status:
            abort(422, "Status duplicated")
        try:
            product_status = ProductStatus(name=product_status_data['name'],
                                           active=product_status_data['active']
                                           )

            db.session.add(product_status)
            db.session.commit()
        except ValueError as ve:
            abort(400, "Bad Request: " + ve.__str__())
        response_data = jsonify({'product_status': product_status.to_dict()})

        return make_response(response_data, 201)

    def delete(self, id: int = None):
        product_status = ProductStatus.query.filter_by(
            id=id).first() or abort(404)
        if product_status:
            db.session.delete(product_status)
            db.session.commit()

        return make_response("ProductStatus was deleted", 200)
