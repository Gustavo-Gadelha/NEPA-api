from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden

from app.jwt import requires_any
from app.models.enums import Autoridade
from app.schemas import UsuarioOutSchema, UsuarioInSchema
from app.services import usuario_service

usuario_bp = Blueprint('usuario', __name__, description='Rotas que modificam usuários')


@usuario_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        raise Forbidden('Acesso negado, usuário não está ativo')

    return None


@usuario_bp.route('/<uuid:usuario_id>/ativar', methods=['POST'])
@requires_any(Autoridade.ADMIN)
@usuario_bp.response(200)
def ativar_usuario(usuario_id):
    usuario_service.alterar_ativacao(usuario_id, True)
    return jsonify({'message': 'Usuário ativado com sucesso'}), 200


@usuario_bp.route('/<uuid:usuario_id>/desativar', methods=['POST'])
@requires_any(Autoridade.ADMIN)
@usuario_bp.response(200, UsuarioOutSchema)
def desativar_usuario(usuario_id):
    usuario_service.alterar_ativacao(usuario_id, False)
    return jsonify({'message': 'Usuário desativado com sucesso'}), 200


@usuario_bp.route('/<uuid:usuario_id>/senha', methods=['PATCH'])
@requires_any(Autoridade.ADMIN)
@usuario_bp.arguments(UsuarioInSchema(only=['senha']))
@usuario_bp.response(200)
def atualizar_senha_usuario(args, usuario_id):
    senha = args.get('senha')
    usuario_service.alterar_senha(usuario_id, senha)
    return jsonify({'message': 'Senha redefinida com sucesso'}), 200
