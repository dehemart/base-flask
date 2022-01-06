from flask_login import LoginManager
from flask import abort
from werkzeug.security import check_password_hash

from base.models.user import User

login_manager = LoginManager()


def init_app(app):
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.request_loader
    def load_request(request):
        api_key = request.headers.get('api_key')
        username = request.headers.get('username')
        user = User.query.filter_by(username=username).first()

        if check_password_hash(user.api_key, api_key):
            return user
        else:
            abort(401, "User not authorized")

    @ login_manager.unauthorized_handler
    def unauthorized():
        abort(401, "User not authorized")
