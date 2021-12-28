from base.extensions.database import db
from sqlalchemy_serializer import SerializerMixin
from dynaconf import settings
from sqlalchemy_utils import force_auto_coercion


force_auto_coercion()


class UserStatus(db.Model, SerializerMixin):
    __tablename__ = 'user_status'
    __table_args__ = {"schema": settings.DB_SCHEMA}
    serialize_only = ('id', 'name', 'active')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    active = db.Column(db.Boolean, default=False)

    created = db.Column(db.TIMESTAMP(True), server_default=db.func.now())
    updated = db.Column(db.TIMESTAMP(True), server_default=db.func.now(),
                        server_onupdate=db.func.now())

