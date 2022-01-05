from base.blueprints import restapi


def init_app(app):
    restapi.init_app(app)
    app.register_blueprint(restapi.blueprint)
