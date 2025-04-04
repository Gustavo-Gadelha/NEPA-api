from uuid import UUID

from flask_jwt_extended.exceptions import JWTDecodeError

from app import jwt, db
from app.models.usuarios import Usuario


@jwt.user_identity_loader
def get_jwt_identity(usuario: Usuario) -> str:
    return usuario.id.hex


@jwt.additional_claims_loader
def add_claims(usuario: Usuario) -> dict[str, str]:
    return {'autoridade': usuario.autoridade.value}


@jwt.user_lookup_loader
def user_lookup_loader(jwt_header, jwt_payload):
    identidade = jwt_payload.get('sub')

    try:
        uuid = UUID(identidade)
    except ValueError:
        raise JWTDecodeError('Formato do UUID inválido enviado no token')

    usuario = db.session.scalar(db.select(Usuario).where(Usuario.id == uuid))
    return usuario if usuario and usuario.ativo else None
