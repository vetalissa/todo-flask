from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# db = SQLAlchemy()

def create_app():
    """ Create app for Flask project. """
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = 'sdfn32kln4kdnwfsk4nfkeden'

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'

    # db.init_app(app)

    # Routers
    from apps.todoapps.core.routers import core
    from apps.todoapps.users.routers import users
    from apps.todoapps.todos.routers import todos

    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(todos, url_prefix='/todos')


    # Migrate(app=app, db=db)

    return app