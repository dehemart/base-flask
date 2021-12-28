from flask import Blueprint
from flask_restful import Api

from base.blueprints.restapi.user_resource import UserResource
from base.blueprints.restapi.product_resource import ProductResource
from base.blueprints.restapi.user_status_resource import UserStatusResource
from base.blueprints.restapi.product_status_resource import ProductStatusResource
from base.blueprints.restapi.product_category_resource import ProductCategoryResource

bp = Blueprint('restapi', __name__, url_prefix='/api/v1')

api = Api(bp)


def init_app(app):

    api.add_resource(UserResource, '/users/', '/users/<id>')
    api.add_resource(UserStatusResource, '/users/statuses',
                     '/users/statuses/<id>')

    api.add_resource(ProductResource, '/products/', '/products/<id>')
    api.add_resource(ProductStatusResource,
                     '/products/statuses', '/products/statuses/<id>')
    api.add_resource(ProductCategoryResource,
                     '/products/categories', '/products/categories/<id>')
    app.register_blueprint(bp)
