from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from dynaconf import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
engine.execute(settings.DB_SCHEMA_CREATE)

db = SQLAlchemy()


def ini_app(app):
    db.init_app(app)
