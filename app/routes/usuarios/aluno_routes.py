from flask import jsonify
from flask_smorest import Blueprint

from app.jwt import requires_any
from app.models.enums import Autoridade
from app.schemas import AlunoInSchema, AlunoOutSchema
from app.services import aluno_service

aluno_bp = Blueprint('aluno', __name__, description='Rotas que modificam alunos')


@aluno_bp.route('/', methods=['POST'])
@requires_any(Autoridade.ADMIN)
@aluno_bp.arguments(AlunoInSchema)
@aluno_bp.response(201, AlunoOutSchema)
def criar_aluno(aluno):
    return aluno_service.save(aluno)


@aluno_bp.route('/', methods=['GET'])
@requires_any(Autoridade.ADMIN)
@aluno_bp.response(200, AlunoOutSchema(many=True))
def listar_alunos():
    return aluno_service.get_all()


@aluno_bp.route('/<uuid:aluno_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN)
@aluno_bp.response(200, AlunoOutSchema)
def exibir_aluno_id(aluno_id):
    return aluno_service.get_or_404(aluno_id)


@aluno_bp.route('/<uuid:aluno_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
@aluno_bp.response(200)
def deletar_aluno(aluno_id):
    aluno_service.delete(aluno_id)
    return jsonify({'message': 'Aluno deletado com sucesso'}), 200
