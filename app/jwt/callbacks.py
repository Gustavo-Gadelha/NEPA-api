from typing import Any
from uuid import UUID

from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTDecodeError

from app.extensions import db
from app.models.usuarios import Usuario


def register_jwt_callbacks(jwt: JWTManager) -> None:
    @jwt.user_identity_loader
    def get_jwt_identity(usuario: Usuario) -> str:
        return str(usuario.id)

    @jwt.user_lookup_loader
    def user_lookup_loader(jwt_header, jwt_data) -> Usuario | None:
        identidade = jwt_data.get('sub')

        try:
            uuid = UUID(identidade)
        except ValueError:
            raise JWTDecodeError('Formato do UUID inválido enviado no token')

        usuario = db.session.scalar(db.select(Usuario).where(Usuario.id == uuid))
        return usuario if usuario and usuario.ativo else None

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
        return jsonify({'message': 'Não foi possível localizar o usuário associado a este token'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'message': 'O stoken JWT expirou, faça login novamente'}), 401

    @jwt.unauthorized_loader
    def unauthorized_token_callback(reason):
        return jsonify({'message': 'Token JWT não econtrado na requisição', 'error': reason}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({'message': 'Token JWT não inválido na requisição', 'error': reason}), 401
