from flask import jsonify
from flask_jwt_extended import current_user, jwt_required
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden

from app.jwt import requires_any
from app.models import Professor
from app.models.enums import Autoridade
from app.schemas import ProfessorInSchema, ProfessorOutSchema
from app.services import professor_service

professor_bp = Blueprint('professor', __name__, description='Rotas que modificam professores')


@professor_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        raise Forbidden('Acesso negado, usuário não está ativo')

    return None


@professor_bp.route('/', methods=['POST'])
@requires_any(Autoridade.ADMIN)
@professor_bp.arguments(ProfessorInSchema)
@professor_bp.response(201, ProfessorOutSchema)
def criar_professor(professor):
    return professor_service.save(professor)


@professor_bp.route('/', methods=['GET'])
@requires_any(Autoridade.ADMIN)
@professor_bp.response(200, ProfessorOutSchema(many=True))
def listar_professores():
    return professor_service.get_all()


@professor_bp.route('/<uuid:professor_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN)
@professor_bp.response(200, ProfessorOutSchema)
def exibir_professor_id(professor_id):
    return professor_service.get_or_404(professor_id)


@professor_bp.route('/<uuid:professor_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
@professor_bp.response(200)
def deletar_professor(professor_id):
    professor_service.delete(professor_id)
    return jsonify({'message': 'Professor deletado com sucesso'}), 200


@professor_bp.route('/ativos', methods=['GET'])
@requires_any(Autoridade.ADMIN)
@professor_bp.response(200, ProfessorOutSchema(many=True))
def listar_professores_ativos():
    return professor_service.get_all(Professor.ativo == True)


@professor_bp.route('/desativos', methods=['GET'])
@requires_any(Autoridade.ADMIN)
@professor_bp.response(200, ProfessorOutSchema(many=True))
def listar_professores_desativos():
    return professor_service.get_all(Professor.ativo == False)
