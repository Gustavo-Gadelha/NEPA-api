import os

from flask import Flask


def create_app(env: str = None) -> Flask:
    app = Flask(__name__)
    from . import config

    match env or os.getenv('FLASK_ENV', default='production'):
        case 'production':
            app.config.from_object(config.ProductionConfig)
        case 'development':
            app.config.from_object(config.DevelopmentConfig)
        case 'testing':
            app.config.from_object(config.TestingConfig)
        case _:
            raise RuntimeError(f"Ambiente de execução '{env}' não reconhecido")

    from app.extensions import db, migrate, jwt_manager, argon2, api
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)
    argon2.init_app(app)
    api.init_app(app)

    # Reference for Flask-CORS configuration and usage:
    # https://corydolphin.com/flask-cors/extension/
    from flask_cors import CORS
    CORS(app)

    from app import models
    from app import schemas
    from app import services

    from app.handlers import register_error_handlers
    register_error_handlers(app)

    from app.jwt import register_jwt_callbacks
    register_jwt_callbacks(jwt_manager)

    from app.routes import register_blueprints
    register_blueprints(api)

    return app
