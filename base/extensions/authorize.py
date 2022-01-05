from flask_login import LoginManager

from base.models.user import User


def init_app(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(self, user_id):
        return User.query.get(int(user_id))
