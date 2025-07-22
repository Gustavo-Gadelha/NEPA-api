from typing import Any
from uuid import UUID

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTDecodeError, UserLookupError
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import Unauthorized

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
            'tipo': usuario.tipo
        }

    @jwt.user_lookup_error_loader
    def user_lookup_error_callback(jwt_header, jwt_payload):
        identidade = jwt_payload.get('sub')
        app.logger.warning(f'Erro ao buscar usuário com UUID: {identidade}')
        raise Unauthorized('Não foi possível localizar o usuário associado a este token')

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        identidade = jwt_payload.get('sub')
        app.logger.info(f'Token expirado para usuário com UUID: {identidade}')
        raise Unauthorized('O token JWT expirou, faça login novamente')

    @jwt.unauthorized_loader
    def unauthorized_token_callback(reason):
        app.logger.warning(f'Requisição sem token JWT: {reason}')
        raise Unauthorized('Token JWT não encontrado na requisição')

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        app.logger.warning(f'Token JWT inválido: {reason}')
        raise Unauthorized('Token JWT inválido na requisição')

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        identidade = jwt_payload.get('sub')
        app.logger.warning(f'Token revogado para usuário com UUID: {identidade}')
        raise Unauthorized('Este token foi revogado, faça login novamente')
