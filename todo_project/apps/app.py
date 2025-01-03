from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    """ Create app for Flask project. """

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
    app.secret_key = 'sdfn32kln4kdnwfsk4nfkeden'

    db.init_app(app)

    # Users
    login_manager = LoginManager()
    login_manager.init_app(app)

    from apps.todoapps.users.models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('core.index'))

    bcrypt.init_app(app)

    # Routers
    from apps.todoapps.core.routers import core
    from apps.todoapps.todos.routers import todos
    from apps.todoapps.users.routers import create_user_blueprint

    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(create_user_blueprint(bcrypt), url_prefix='/users', bcrypt=bcrypt)
    app.register_blueprint(todos, url_prefix='/todos')

    migrate.init_app(app, db)

    return app
