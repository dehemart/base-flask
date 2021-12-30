import click
import sqlalchemy
from werkzeug.security import generate_password_hash

from base.extensions.database import db
from base.models.user import User, UserStatus


def init_app(app):
    db.init_app(app)

    @app.cli.command()
    def create_db():
        """Create database structure"""
        db.create_all()

    @app.cli.command()
    def drop_db():
        """Drop database structure"""
        db.drop_all()

    @app.cli.command()
    def init_db():
        """ Populate database with initial data """
        user = add_user()
        db.session.add(user)
        db.session.commit()

    @app.cli.command()
    def reset_db():
        """ Recreate DB with initial data """
        db.drop_all()
        db.create_all()

        add_user_status()
        user_status_active = add_user_status('ACTIVE')
        add_user('admin', 'admin', 'admin@email', user_status_active)

    @app.cli.command()
    @click.option("--username", "-u", default="admin", help='User name for login')
    @click.option("--password", "-p", default="admin", help='User password for login')
    @click.option("--email", "-e", default="admin@admin", help='User email for comunicaiton')
    def new_user(username: str = "admin", password: str = "admin", email: str = "admin@admin"):
        """ Create user to access this app """
        try:
            add_user_status()
            user_status_active = add_user_status('ACTIVE')
            add_user(username, password, email, user_status_active)
        except sqlalchemy.exc.IntegrityError:
            print("User already exists")
        except sqlalchemy.exc.OperationalError:
            print("Database error")
        except Exception as e:
            print(f"Error on execute command: {e._message}")

    def add_user(username: str = "admin", password: str = "admin", email: str = "admin@admin", status: UserStatus = None):
        if status:
            status_id = status.id
        else:
            status_id = 1
        user = User(username=username,
                    password=generate_password_hash(password),
                    email=email,
                    status_id=status_id)
        db.session.add(user)
        db.session.commit()

    def add_user_status(name: str = "CREATED"):
        user_status = UserStatus(name=name, active=True)
        db.session.add(user_status)
        db.session.commit()
        return user_status
