from flask_jwt_extended import create_refresh_token, create_access_token

from app import db, argon2
from app.models import Usuario


def login(login: str, senha: str) -> Usuario | None:
    usuario: Usuario = get_usuario(login)
    if usuario and argon2.check_password_hash(usuario.senha, senha):
        return usuario

    return None


def access_token(usuario: Usuario) -> str:
    return create_access_token(identity=usuario)


def refresh_token(usuario: Usuario) -> str:
    return create_refresh_token(identity=usuario)


def get_usuario(login: str) -> Usuario:
    if '@' in login:
        stmt = db.select(Usuario).where(Usuario.email == login)
    else:
        stmt = db.select(Usuario).where(Usuario.matricula == login)

    return db.session.scalar(stmt)
