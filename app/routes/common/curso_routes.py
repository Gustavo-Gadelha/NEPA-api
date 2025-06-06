from flask import request, jsonify
from flask_jwt_extended import current_user, jwt_required
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden

from app.jwt import requires_any
from app.models.enums import Autoridade
from app.schemas import CursoInSchema, CursoOutSchema
from app.services import curso_service

curso_bp = Blueprint('curso', __name__, description='Rotas que modificam cursos')


@curso_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        raise Forbidden('Acesso negado, usuário não está ativo')

    return None


@curso_bp.route('/', methods=['POST'])
@requires_any(Autoridade.ADMIN)
@curso_bp.arguments(CursoInSchema)
@curso_bp.response(201, CursoOutSchema)
def criar_curso():
    dados = request.json
    return curso_service.save(dados)


@curso_bp.route('/', methods=['GET'])
@curso_bp.response(200, CursoOutSchema(many=True))
def listar_cursos():
    return curso_service.get_all()


@curso_bp.route('/<uuid:curso_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN)
@curso_bp.response(200, CursoOutSchema)
def exibir_curso_id(curso_id):
    return curso_service.get_or_404(curso_id)


@curso_bp.route('/<uuid:curso_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
@curso_bp.response(200)
def deletar_curso(curso_id):
    curso_service.delete(curso_id)
    return jsonify({'message': 'Curso deletado com sucesso'}), 200
