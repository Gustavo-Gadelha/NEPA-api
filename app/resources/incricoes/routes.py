from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import Conflict, Forbidden

from app.jwt import requires_any
from app.models import Inscricao, Projeto, Usuario
from app.models.enums import Autoridade, StatusProjeto

from .schemas import InscricaoOutSchema, InscricaoPatchInSchema, InscricaoQueryArgsSchema
from .services import inscricao_service

inscricao_blp = Blueprint('inscricoes', __name__, description='Modulo de inscrições')


@inscricao_blp.route('/')
class InscricaoList(MethodView):

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @inscricao_blp.arguments(InscricaoQueryArgsSchema, location='query', as_kwargs=True)
    @inscricao_blp.response(200, InscricaoOutSchema(many=True))
    def get(self, projeto_id, **kwargs):
        projeto = Projeto.objects.get_or_404(projeto_id)

        if not Usuario.access.is_owner(projeto.professor_id):
            raise Forbidden('Este professor não pode acessar as incrições deste projeto')

        return inscricao_service.get_all(**kwargs)

    @requires_any(Autoridade.ALUNO)
    @inscricao_blp.response(200, InscricaoOutSchema)
    def post(self, projeto_id):
        projeto = Projeto.objects.get_or_404(projeto_id)

        if not projeto.status == StatusProjeto.EM_ANDAMENTO:
            raise Conflict('Este projeto ainda não está em andamento')
        if inscricao_service.exists_for(projeto_id, current_user.id):
            raise Conflict('O aluno já está inscrito neste projeto')
        if projeto.vagas_ocupadas >= projeto.vagas_totais:
            raise Conflict('Não há vagas disponiveis para este projeto')

        inscricao = Inscricao(projeto_id=projeto_id, aluno_id=current_user.id)
        projeto.vagas_ocupadas += 1

        return inscricao_service.save(inscricao)


@inscricao_blp.route('/<incricao_id>')
class InscricaoDetail(MethodView):

    @requires_any(Autoridade.PROFESSOR)
    @inscricao_blp.response(200, InscricaoOutSchema)
    def get(self, projeto_id, incricao_id):
        projeto = Projeto.objects.get_or_404(projeto_id)

        if not Usuario.access.is_owner(projeto.professor_id):
            raise Forbidden('Este professor não pode acessar está inscrição')

        return inscricao_service.get(incricao_id)

    @requires_any(Autoridade.PROFESSOR)
    @inscricao_blp.arguments(InscricaoPatchInSchema)
    @inscricao_blp.response(200, InscricaoOutSchema)
    def patch(self, dados, projeto_id, incricao_id):
        projeto = Projeto.objects.get_or_404(projeto_id)

        if not Usuario.access.is_owner(projeto.professor_id):
            raise Forbidden('Este professor não pode acessar está inscrição')

        return inscricao_service.patch(incricao_id, dados)
