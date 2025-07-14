from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden, Conflict

from app.jwt import requires_any
from app.models import Projeto, Inscricao
from app.models.enums import Autoridade, StatusProjeto
from app.resources.projetos import projeto_service
from .schemas import InscricaoPatchInSchema, InscricaoOutSchema
from .services import inscricao_service

inscricao_blp = Blueprint('inscricoes', __name__, description='Modulo de inscrições')


@inscricao_blp.route('/')
class InscricaoList(MethodView):

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @inscricao_blp.response(200, InscricaoOutSchema(many=True))
    def get(self, projeto_id):
        projeto: Projeto = projeto_service.get_or_404(projeto_id)

        if current_user.autoridade == Autoridade.ADMIN:
            return inscricao_service.get_all(projeto_id=projeto_id)
        if not current_user.id == projeto.professor_id:
            raise Forbidden

        return inscricao_service.get_all(projeto_id=projeto_id)

    @requires_any(Autoridade.ALUNO)
    @inscricao_blp.response(200, InscricaoOutSchema)
    def post(self, projeto_id):
        projeto = projeto_service.get_or_404(projeto_id)

        if not projeto.status == StatusProjeto.EM_ANDAMENTO:
            raise Conflict('Este projeto ainda não está em andamento')
        if projeto.vagas_ocupadas >= projeto.vagas_totais:
            raise Conflict('Não há vagas disponiveis para este projeto')
        if inscricao_service.exists_for(projeto_id, current_user.id):
            raise Conflict('O aluno já está inscrito neste projeto')

        inscricao = Inscricao(projeto_id=projeto_id, aluno_id=current_user.id)

        projeto.vagas_ocupadas += 1
        return inscricao_service.save(inscricao)


@inscricao_blp.route('/<incricao_id>')
class InscricaoDetail(MethodView):

    @requires_any(Autoridade.PROFESSOR)
    @inscricao_blp.response(200, InscricaoOutSchema)
    def get(self, projeto_id, incricao_id):
        if not projeto_service.is_owner(projeto_id, current_user):
            raise Forbidden('Este professor não pode alterar este projeto')

        return inscricao_service.get(incricao_id)

    @requires_any(Autoridade.PROFESSOR)
    @inscricao_blp.arguments(InscricaoPatchInSchema)
    @inscricao_blp.response(200, InscricaoOutSchema)
    def patch(self, projeto_id, incricao_id, dados):
        if not projeto_service.is_owner(projeto_id, current_user):
            raise Forbidden('Este professor não pode alterar este projeto')

        return inscricao_service.patch(incricao_id, dados)
