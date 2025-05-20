from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, current_user

from app.models.enums import Autoridade


def requires_any(*autoridades: Autoridade):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            if current_user.autoridade not in autoridades:
                return jsonify({'message': 'Acesso negado, você não tem permissão para acessar este recurso'}), 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper


def forbids_any(*autoridades: Autoridade):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            if current_user.autoridade in autoridades:
                return jsonify({'message': 'Acesso negado, você não tem permissão para acessar este recurso'}), 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper
