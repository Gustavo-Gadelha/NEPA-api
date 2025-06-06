from flask import Flask
from flask_jwt_extended import get_jwt_identity, current_user, verify_jwt_in_request
from werkzeug.exceptions import Forbidden


def register_interceptors(app: Flask):
    @app.before_request
    def verify_user_is_active():
        verify_jwt_in_request(optional=True)
        if get_jwt_identity() and not current_user.ativo:
            raise Forbidden('Este usuário está desativado')

        return None