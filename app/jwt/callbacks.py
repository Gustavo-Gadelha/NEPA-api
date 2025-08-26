from typing import Any
from uuid import UUID

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTDecodeError
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import Forbidden, Unauthorized

from app.models.usuarios import Usuario


def register_jwt_callbacks(app: Flask, db: SQLAlchemy, jwt: JWTManager) -> None:
    @jwt.user_identity_loader
    def get_jwt_identity(usuario: Usuario) -> str:
        return str(usuario.id)

    @jwt.user_lookup_loader
    def user_lookup_loader(jwt_header, jwt_data) -> Usuario | None:
        identity = jwt_data.get('sub')

        if identity is None:
            app.logger.warning(f'UUID não encontrado no token: {jwt_data}')
            raise JWTDecodeError('UUID não encontrado no token')

        try:
            uuid = UUID(identity)
        except ValueError as ve:
            raise JWTDecodeError('Formato do UUID inválido enviado no token') from ve

        usuario = db.session.get(Usuario, uuid)

        if not usuario:
            app.logger.info(f'Usuário com UUID {uuid} não encontrado')
            raise Unauthorized('Usuário não encontrado')
        if not usuario.ativo:
            app.logger.info(f'Usuário com UUID {uuid} está inativo')
            raise Forbidden('Usuário está inativo')

        return usuario

    @jwt.additional_claims_loader
    def add_claims(usuario: Usuario) -> dict[str, Any]:
        return {
            'nome': usuario.nome,
            'ativo': usuario.ativo,
            'autoridade': usuario.autoridade.value,
            'tipo': usuario.tipo,
        }
