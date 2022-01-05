from black import err
from base.extensions import command, database, error, authorize


def init_app(app):
    database.ini_app(app)
    error.init_app(app)
    command.init_app(app)
    authorize.init_app(app)
    
