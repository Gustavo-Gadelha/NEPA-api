from flask import request, jsonify, Blueprint
from flask_jwt_extended import current_user, jwt_required
from werkzeug.exceptions import Forbidden

from app.config import PASSWORD_LENGTH
from app.decorators import requires_any
from app.models import Aluno
from app.models.enums import Autoridade
from app.schemas import aluno_schema
from app.services.usuarios import aluno_service, usuario_service

aluno_bp = Blueprint('aluno', __name__)


@aluno_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        raise Forbidden('Acesso negado, usuário não está ativo')

    return None


@aluno_bp.route('/', methods=['POST'])
@requires_any(Autoridade.ADMIN)
def criar_aluno():
    dados = request.json
    aluno = aluno_service.save(dados)

    return jsonify(aluno_schema.dump(aluno)), 201


@aluno_bp.route('/', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def listar_alunos():
    alunos: list[Aluno] = aluno_service.get_all()
    return jsonify(aluno_schema.dump(alunos, many=True)), 200


@aluno_bp.route('/<uuid:aluno_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def exibir_aluno_id(aluno_id):
    aluno: Aluno = aluno_service.get_or_404(aluno_id)
    return jsonify(aluno_schema.dump(aluno)), 200


@aluno_bp.route('/<uuid:aluno_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
def deletar_aluno(aluno_id):
    aluno_service.delete(aluno_id)
    return jsonify({'message': 'Aluno deletado com sucesso'}), 200


@aluno_bp.route('/<uuid:aluno_id>/senha>', methods=['PATCH'])
@requires_any(Autoridade.ADMIN)
def redefinir_senha_aluno(aluno_id):
    dados = request.json
    senha = dados.get('senha')

    if not aluno_service.is_valid_password(senha):
        return jsonify({'message': f'Senha inválida. A senha deve ter pelo menos {PASSWORD_LENGTH} caracteres'}), 400

    usuario_service.change_password(aluno_id, senha)
    return jsonify({'message': 'Senha redefinida com sucesso'}), 200
