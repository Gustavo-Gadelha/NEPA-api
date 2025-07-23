from collections.abc import Callable
from functools import wraps

from flask_jwt_extended import current_user, verify_jwt_in_request
from werkzeug.exceptions import Forbidden

from app.models.enums import Autoridade


def authorize(*autoridades: Autoridade, permitir: bool = True) -> Callable:
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            tem_autoridade = current_user.autoridade in autoridades

            if permitir and not tem_autoridade:
                raise Forbidden('Você não tem autorização para realizar esta ação')
            if not permitir and tem_autoridade:
                raise Forbidden('Você não tem autorização para realizar esta ação')

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def requires_any(*autoridades: Autoridade) -> Callable:
    return authorize(*autoridades, permitir=True)


def forbids_any(*autoridades: Autoridade) -> Callable:
    return authorize(*autoridades, permitir=False)
