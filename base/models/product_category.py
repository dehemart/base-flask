from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_utils import force_auto_coercion
from dynaconf import settings

from base.extensions.database import db

force_auto_coercion()


class ProductCategory(db.Model, SerializerMixin):
    __tablename__ = 'product_category'
    __table_args__ = {"schema": settings.DB_SCHEMA}
    serialize_only = ('id', 'name', 'active')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    active = db.Column(db.Boolean, default=False)

    created = db.Column(db.TIMESTAMP(True), server_default=db.func.now())
    updated = db.Column(db.TIMESTAMP(True), server_default=db.func.now(),
                        server_onupdate=db.func.now())
