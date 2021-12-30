from flask import abort, jsonify, make_response, request
from werkzeug.security import generate_password_hash
from flask_restful import Resource

from base.models.user import User
from base.extensions.database import db


class UserResource(Resource):
    """" API Resource of User """

    def get(self, id: int = None):
        if id:
            return self._get_one(id)
        else:
            return self._get_all()

    def _get_all(self):
        users = User.query.all() or abort(400, "Users not found")
        response_data = jsonify(
            {'users': [user.to_dict() for user in users]})
        return make_response(response_data, 200)

    def _get_one(self, id: int):
        user = User.query.get(
            id) or abort(404, "User not found")
        response_data = jsonify({'user': user.to_dict()})
        return make_response(response_data, 200)

    def put(self, id: int = None):
        user_data = request.get_json()

        if id:
            user = User.query.filter_by(id=id).first()
        else:
            user = None
        try:
            if user:
                return_code = 200
                user.username = user_data['username'].lower(
                ) if user_data['username'] is None else user.username
                user.password = generate_password_hash(
                    user_data['password']) if user_data['password'] is not None else user.password
                user.email = user_data['email'] if user_data['email'] is not None else user.email
                user.status_id = user_data['status_id'] if user_data['status_id'] is not None else user.status_id
            else:
                return_code = 201
                user = User(username=user_data['username'].lower(),
                            password=generate_password_hash(
                                user_data['password']),
                            email=user_data['email'],
                            status_id=user_data['status_id'])
            db.session.add(user)
            db.session.commit()
        except ValueError as ve:
            abort(400, "Bad Request: " + ve.__str__())
        response_data = jsonify(
            {'user': user.to_dict()}
        )
        return make_response(response_data, return_code)

    def post(self):
        user_data = request.get_json()

        user = User.query.filter_by(
            username=user_data['username']).first()
        if user:
            abort(422, "Username duplicated")
        try:
            user = User(username=user_data['username'],
                        password=generate_password_hash(user_data['password']),
                        email=user_data['email'],
                        status_id=user_data['status_id'])

            db.session.add(user)
            db.session.commit()
        except ValueError as ve:
            abort(400, "Bad Request: " + ve.__str__())
        response_data = jsonify({'user': user.to_dict()})

        return make_response(response_data, 201)

    def delete(self, id: int = None):
        user = User.query.filter_by(id=id).first() or abort(404)
        if user:
            db.session.delete(user)
            db.session.commit()

        return make_response("User was deleted", 200)
