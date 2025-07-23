from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import EXCLUDE, ValidationError
from werkzeug.exceptions import Unauthorized

from app.jwt import requires_any
from app.models.enums import Autoridade
from app.resources.alunos import AlunoInSchema
from app.resources.professores import ProfessorInSchema

from .schemas import LoginInSchema, RedefinirSenhaInSchema, RegisterInSchema, TokensOutSchema
from .services import auth_service

auth_blp = Blueprint('auth', __name__, url_prefix='/auth', description='Modulo de autenticação')


@auth_blp.route('/login')
class LoginResource(MethodView):

    @auth_blp.arguments(LoginInSchema)
    @auth_blp.response(200, TokensOutSchema)
    def post(self, credenciais):
        login = credenciais.get('login')
        senha = credenciais.get('senha')

        usuario = auth_service.login(login, senha)
        if usuario is None:
            raise Unauthorized('Credenciais inválidas')

        return auth_service.create_tokens(usuario)


@auth_blp.route('/register')
class RegisterResource(MethodView):

    @auth_blp.arguments(RegisterInSchema)
    @auth_blp.response(200, TokensOutSchema)
    def post(self, dados):
        match dados.get('tipo'):
            case 'aluno':
                schema = AlunoInSchema(unknown=EXCLUDE)
            case 'professor':
                schema = ProfessorInSchema(unknown=EXCLUDE)
            case _:
                raise ValidationError('Tipo de usuário inválido para cadastro')

        usuario = auth_service.register(schema, dados)
        return auth_service.create_tokens(usuario)


@auth_blp.route('/reset-password')
class RedefinirSenhaResource(MethodView):

    @requires_any(Autoridade.ADMIN)
    @auth_blp.arguments(RedefinirSenhaInSchema)
    @auth_blp.response(204)
    def post(self, dados):
        usuario_id = dados.get('usuario_id')
        senha = dados.get('senha')
        return auth_service.reset_password(usuario_id, senha)
