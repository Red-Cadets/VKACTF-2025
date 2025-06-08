from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    from config.config import Config
    app.config.from_object(Config)

    db.init_app(app)


    from .routes import init_routes
    from .auth import init_auth

    init_routes(app)
    init_auth(app)

    with app.app_context():
        db.create_all()

    return app

