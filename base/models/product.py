from base.extensions.database import db
from sqlalchemy_serializer import SerializerMixin
from dynaconf import settings
from sqlalchemy_utils import force_auto_coercion

from base.models.product_status import ProductStatus
from base.models.product_category import ProductCategory

force_auto_coercion()


class Product(db.Model, SerializerMixin):
    __tablename__ = 'product'
    __table_args__ = {"schema": settings.DB_SCHEMA}
    serialize_only = ('id', 'sku', 'name', 'description',
                      'status', 'category')

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(250), index=True)
    name = db.Column(db.String(250), index=True)
    description = db.Column(db.String(250))

    status_id = db.Column(db.Integer, db.ForeignKey(f'{settings.DB_SCHEMA}.product_status.id'),
                          nullable=False)
    status = db.relationship('ProductStatus')

    category_id = db.Column(db.Integer, db.ForeignKey(f'{settings.DB_SCHEMA}.product_category.id'),
                            nullable=False)
    category = db.relationship('ProductCategory')

    created = db.Column(db.TIMESTAMP(True), server_default=db.func.now())
    updated = db.Column(db.TIMESTAMP(True), server_default=db.func.now(),
                        server_onupdate=db.func.now())
