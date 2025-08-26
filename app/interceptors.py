from typing import Any

from flask import Flask
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from werkzeug.exceptions import Forbidden


def register_interceptors(app: Flask):
    @app.before_request
    def verify_user_is_active():
        verify_jwt_in_request(optional=True)
        claims: dict[str, Any] | None = get_jwt()

        if not claims:
            return
        if not claims.get('ativo', False):
            raise Forbidden('Este usuário está desativado')
