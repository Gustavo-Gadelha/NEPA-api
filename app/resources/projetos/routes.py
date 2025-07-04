from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden, Conflict

from app.jwt import requires_any
from app.models import Projeto
from app.models.enums import Autoridade, StatusProjeto
from .schemas import (
    ProjetoInSchema,
    ProjetoQueryArgsSchema,
    ProjetoPatchInSchema,
    ProjetoOutSchema,
    InscricaoInSchema,
    InscricaoPatchInSchema,
    InscricaoOutSchema
)
from .services import projeto_service, inscricao_service

projeto_blp = Blueprint('projetos', __name__, url_prefix='/projetos', description='Modulo de projetos')


@projeto_blp.route('/')
class ProjetoList(MethodView):

    @projeto_blp.arguments(ProjetoQueryArgsSchema, location='query', as_kwargs=True)
    @projeto_blp.response(200, ProjetoOutSchema(many=True))
    def get(self, **kwargs):
        return projeto_service.get_all(**kwargs)

    @requires_any(Autoridade.PROFESSOR)
    @projeto_blp.arguments(ProjetoInSchema)
    @projeto_blp.response(201, ProjetoOutSchema)
    def post(self, projeto):
        return projeto_service.save(projeto)


@projeto_blp.route('/me')
class ProjetoMe(MethodView):

    @requires_any(Autoridade.PROFESSOR)
    @projeto_blp.response(200, ProjetoOutSchema(many=True))
    def get(self):
        return projeto_service.get_all(professor_id=current_user.id)


@projeto_blp.route('/<uuid:projeto_id>')
class ProjetoDetail(MethodView):

    @projeto_blp.response(200, ProjetoOutSchema)
    def get(self, projeto_id):
        return projeto_service.get_or_404(projeto_id)

    @requires_any(Autoridade.ADMIN)
    @projeto_blp.arguments(ProjetoPatchInSchema)
    @projeto_blp.response(200, ProjetoOutSchema)
    def patch(self, projeto_id, dados):
        return projeto_service.update(projeto_id, dados)

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @projeto_blp.response(204)
    def delete(self, projeto_id):
        projeto: Projeto = projeto_service.get_or_404(projeto_id)

        if current_user.autoridade == Autoridade.ADMIN:
            return projeto_service.delete(projeto)
        if not current_user.id == projeto.professor_id:
            raise Forbidden

        return projeto_service.delete(projeto)


inscricao_blp = Blueprint('inscricoes', __name__, description='Modulo de inscrições')


@inscricao_blp.route('/<uuid:projeto_id>/inscricoes')
class InscricaoList(MethodView):

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @projeto_blp.response(200, InscricaoOutSchema(many=True))
    def get(self, projeto_id):
        projeto: Projeto = projeto_service.get_or_404(projeto_id)

        if current_user.autoridade == Autoridade.ADMIN:
            return inscricao_service.get_by_project(projeto_id)
        if not current_user.id == projeto.professor_id:
            raise Forbidden

        return inscricao_service.get_by_project(projeto_id)

    @requires_any(Autoridade.ALUNO)
    @projeto_blp.arguments(InscricaoInSchema)
    @projeto_blp.response(200, InscricaoOutSchema)
    def post(self, projeto_id, inscricao):
        projeto = projeto_service.get_or_404(projeto_id)

        if not projeto.status == StatusProjeto.APROVADO:
            raise Conflict('Este projeto ainda não foi aprovado')
        if projeto.vagas_ocupadas >= projeto.vagas_totais:
            raise Conflict('Não há vagas disponiveis para este projeto')
        if inscricao_service.exists_for(projeto_id, current_user.id):
            raise Conflict('O aluno já está inscrito neste projeto')

        projeto.vagas_ocupadas += 1
        return inscricao_service.save(inscricao)


@inscricao_blp.route('/<uuid:projeto_id>/inscricoes/<incricao_id>')
class InscricaoDetail(MethodView):

    @requires_any(Autoridade.PROFESSOR)
    @projeto_blp.response(200, InscricaoOutSchema)
    def get(self, projeto_id, incricao_id):
        if not projeto_service.is_owner(projeto_id, current_user):
            raise Forbidden('Este professor não pode alterar este projeto')

        return inscricao_service.get(incricao_id)

    @requires_any(Autoridade.PROFESSOR)
    @projeto_blp.arguments(InscricaoPatchInSchema)
    @projeto_blp.response(200, InscricaoOutSchema)
    def patch(self, projeto_id, incricao_id, dados):
        if not projeto_service.is_owner(projeto_id, current_user):
            raise Forbidden('Este professor não pode alterar este projeto')

        return inscricao_service.update(incricao_id, dados)


projeto_blp.register_blueprint(inscricao_blp)
