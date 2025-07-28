from typing import Any
from uuid import UUID

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTDecodeError, UserLookupError
from flask_sqlalchemy import SQLAlchemy

from app.models.usuarios import Usuario


def register_jwt_callbacks(app: Flask, db: SQLAlchemy, jwt: JWTManager) -> None:
    @jwt.user_identity_loader
    def get_jwt_identity(usuario: Usuario) -> str:
        return str(usuario.id)

    @jwt.user_lookup_loader
    def user_lookup_loader(jwt_header, jwt_data) -> Usuario | None:
        identidade = jwt_data.get('sub')
        if identidade is None:
            app.logger.warning(f'Token com UUID inválido: {identidade}')
            raise JWTDecodeError('Formato do UUID inválido enviado no token')

        uuid = UUID(identidade)
        usuario = db.session.get(Usuario, uuid)

        if not usuario:
            app.logger.info(f'Usuário com UUID {uuid} não encontrado')
            raise UserLookupError('Usuário não encontrado', jwt_header, jwt_data)
        elif not usuario.ativo:
            app.logger.info(f'Usuário com UUID {uuid} está inativo')
            raise UserLookupError('Usuário está inativo', jwt_header, jwt_data)

        return usuario

    @jwt.additional_claims_loader
    def add_claims(usuario: Usuario) -> dict[str, Any]:
        return {
            'nome': usuario.nome,
            'ativo': usuario.ativo,
            'autoridade': usuario.autoridade.value,
            'tipo': usuario.tipo,
        }
