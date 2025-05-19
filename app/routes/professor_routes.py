from flask import request, jsonify, Blueprint
from flask_jwt_extended import current_user, jwt_required
from werkzeug.exceptions import Forbidden

from app.config import PASSWORD_LENGTH
from app.decorators import requires_any
from app.models import Professor
from app.models.enums import Autoridade
from app.schemas import professor_schema
from app.services.usuarios import professor_service, usuario_service

professor_bp = Blueprint('professor', __name__)


@professor_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        raise Forbidden('Acesso negado, usuário não está ativo')

    return None


@professor_bp.route('/', methods=['POST'])
@requires_any(Autoridade.ADMIN)
def criar_professor():
    dados = request.json
    professor = professor_service.save(dados)

    return jsonify(professor_schema.dump(professor)), 201


@professor_bp.route('/', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def listar_professores():
    professores: list[Professor] = professor_service.get_all()
    return jsonify(professor_schema.dump(professores, many=True)), 200


@professor_bp.route('/<uuid:professor_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def exibir_professor_id(professor_id):
    professor: Professor = professor_service.get_or_404(professor_id)
    return jsonify(professor_schema.dump(professor)), 200


@professor_bp.route('/<uuid:professor_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
def deletar_professor(professor_id):
    professor_service.delete(professor_id)
    return jsonify({'message': 'Professor deletado com sucesso'}), 200


@professor_bp.route('/<uuid:professor_id>/ativar', methods=['POST'])
def ativar_professor(professor_id):
    usuario_service.activate(professor_id)
    return jsonify({'message': 'Professor ativado com sucesso'}), 200


@professor_bp.route('/<uuid:professor_id>/desativar', methods=['POST'])
def desativar_professor(professor_id):
    usuario_service.deactivate(professor_id)
    return jsonify({'message': 'Professor desativado com sucesso'}), 200


@professor_bp.route('/ativos', methods=['GET'])
def listar_professores_ativos():
    professores: list[Professor] = professor_service.get_all_active()
    return jsonify(professor_schema.dump(professores, many=True)), 200


@professor_bp.route('/desativos', methods=['GET'])
def listar_professores_desativos():
    professores: list[Professor] = professor_service.get_all_inactive()
    return jsonify(professor_schema.dump(professores, many=True)), 200


@professor_bp.route('/<uuid:professor_id>/senha>', methods=['PATCH'])
@requires_any(Autoridade.ADMIN)
def redefinir_senha_professor(professor_id):
    dados = request.json
    senha = dados.get('senha')

    if not senha or len(senha) < PASSWORD_LENGTH:
        return jsonify({'message': f'Senha inválida. A senha deve ter pelo menos {PASSWORD_LENGTH} caracteres'}), 400

    usuario_service.change_password(professor_id, senha)
    return jsonify({'message': 'Senha redefinida com sucesso'}), 200
