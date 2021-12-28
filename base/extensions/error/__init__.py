from black import err
from base.extensions.error import http_errors


def init_app(app):
    http_errors.init_app(app)
