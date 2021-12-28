from flask import Flask
from base.extensions import config

from base import extensions
from base import blueprints


def create_app():
    app = Flask(__name__)
    config.init_app(app)

    extensions.init_app(app)
    blueprints.init_app(app)

    return app
