from flask import abort, jsonify, make_response, request
from flask_login import login_required
from flask_restful import Resource

from base.extensions.database import db
from base.models.user_status import UserStatus


class UserStatusResource(Resource):
    """" API Resource of User """
    decorators = [login_required]

    def get(self, id: int = None):
        if id:
            return self._get_one(id)
        else:
            return self._get_all()

    def _get_all(self):
        user_statuses = UserStatus.query.all() or abort(400, "User Statuses not found")
        response_data = jsonify(
            {'user_status': [user_status.to_dict() for user_status in user_statuses]})
        return make_response(response_data, 200)

    def _get_one(self, id: int):
        user_status = UserStatus.query.filter_by(
            id=id).first() or abort(404, "UserStatus not found")
        response_data = jsonify({'user_status': user_status.to_dict()})
        return make_response(response_data, 200)

    def put(self, id: int = None):
        user_status_data = request.get_json()

        if id:
            user_status = UserStatus.query.filter_by(id=id).first()
        else:
            user_status = None
        try:
            if user_status:
                return_code = 200
                user_status.username = user_status_data['name'] if user_status_data[
                    'name'] is None else user_status.username
                user_status.active = user_status_data['active'] if user_status_data[
                    'active'] is None else user_status.active
            else:
                return_code = 201
                user_status = UserStatus(name=user_status_data['name'],
                                         active=user_status_data['active']
                                         )
            db.session.add(user_status)
            db.session.commit()
        except ValueError as ve:
            abort(400, "Bad Request: " + ve.__str__())
        response_data = jsonify(
            {'user_status': user_status.to_dict()}
        )
        return make_response(response_data, return_code)

    def post(self):
        user_status_data = request.get_json()

        user_status = UserStatus.query.filter_by(
            name=user_status_data['name']).first()
        if user_status:
            abort(422, "Status duplicated")
        try:
            user_status = UserStatus(name=user_status_data['name'],
                                     active=user_status_data['active']
                                     )

            db.session.add(user_status)
            db.session.commit()
        except ValueError as ve:
            abort(400, "Bad Request: " + ve.__str__())
        response_data = jsonify({'user_status': user_status.to_dict()})

        return make_response(response_data, 201)

    def delete(self, id: int = None):
        user_status = UserStatus.query.filter_by(id=id).first() or abort(404)
        if user_status:
            db.session.delete(user_status)
            db.session.commit()

        return make_response("UserStatus was deleted", 200)
