from flask_argon2 import Argon2
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt_manager = JWTManager()
argon2 = Argon2()
api = Api()

from app.handlers import ErrorSchema

# Overrides the default error schema used in OpenAPI docs.
# This is a workaround, but it's the cleanest way to change
# the documented structure of default error (422, 500) responses globally in Flask-Smorest
api.ERROR_SCHEMA = ErrorSchema
