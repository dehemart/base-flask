import flask
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_utils import PasswordType, force_auto_coercion
from dynaconf import settings

from base.extensions.database import db

from base.models.user_status import UserStatus


force_auto_coercion()


class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    __table_args__ = {"schema": settings.DB_SCHEMA}

    serialize_only = ('id', 'username', 'email', 'status')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(
        PasswordType(
            onload=lambda **kwargs: dict(
                schemes=flask.current_app.config['PASSWORD_SCHEMES'],
                **kwargs
            ), deprecated=['md5_crypt']
        ),
        unique=False,
        nullable=False
    )
    email = db.Column(db.String(255), nullable=False)

    status_id = db.Column(db.Integer, db.ForeignKey(f'{settings.DB_SCHEMA}.user_status.id'),
                          nullable=True)

    status = db.relationship("UserStatus")

    created = db.Column(db.TIMESTAMP(True), server_default=db.func.now())
    updated = db.Column(db.TIMESTAMP(True), server_default=db.func.now(),
                        server_onupdate=db.func.now())
