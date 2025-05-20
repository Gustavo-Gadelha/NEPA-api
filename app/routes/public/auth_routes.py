from flask import jsonify
from flask_smorest import Blueprint
from werkzeug.exceptions import NotFound

from app.models.enums import Autoridade
from app.schemas import TokensOutSchema, LoginInSchema, AlunoInSchema, ProfessorInSchema
from app.services import auth_service, aluno_service, professor_service

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
@auth_bp.arguments(LoginInSchema)
@auth_bp.response(200, TokensOutSchema)
def auth_login(credenciais):
    usuario = auth_service.login(credenciais)
    if usuario is None:
        raise NotFound('Credenciais inválidas')

    return auth_service.create_tokens(usuario)


@auth_bp.route('/cadastro/aluno', methods=['POST'])
@auth_bp.arguments(AlunoInSchema)
@auth_bp.response(200)
def auth_cadastrar_aluno(aluno):
    aluno.autoridade = Autoridade.ALUNO
    aluno_service.save(aluno)
    return jsonify({'message': 'Usuário cadastrado com sucesso'}), 200


@auth_bp.route('/cadastro/professor', methods=['POST'])
@auth_bp.arguments(ProfessorInSchema)
@auth_bp.response(200)
def auth_register_professor(professor):
    professor.autoridade = Autoridade.PROFESSOR
    professor_service.save(professor)
    return jsonify({'message': 'Usuário cadastrado com sucesso'}), 200
