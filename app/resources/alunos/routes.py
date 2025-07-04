from flask.views import MethodView
from flask_smorest import Blueprint

from app.jwt import requires_any
from app.models.enums import Autoridade
from .schemas import AlunoQueryArgsSchema, AlunoPatchInSchema, AlunoOutSchema
from .services import aluno_service

aluno_blp = Blueprint('alunos', __name__, url_prefix='/alunos', description='Modulo de alunos')


@aluno_blp.route('/')
class AlunoList(MethodView):

    @requires_any(Autoridade.ADMIN)
    @aluno_blp.arguments(AlunoQueryArgsSchema, location='query', as_kwargs=True)
    @aluno_blp.response(200, AlunoOutSchema(many=True))
    def get(self, **kwargs):
        return aluno_service.get_all(**kwargs)


@aluno_blp.route('/<uuid:aluno_id>')
class AlunoDetail(MethodView):

    @requires_any(Autoridade.ADMIN)
    @aluno_blp.response(200, AlunoOutSchema)
    def get(self, aluno_id):
        return aluno_service.get_or_404(aluno_id)

    @requires_any(Autoridade.ADMIN)
    @aluno_blp.arguments(AlunoPatchInSchema)
    @aluno_blp.response(200, AlunoOutSchema)
    def patch(self, aluno_id, dados):
        return aluno_service.update(aluno_id, dados)

    @requires_any(Autoridade.ADMIN)
    @aluno_blp.response(204)
    def delete(self, aluno_id):
        return aluno_service.delete_by_id(aluno_id)
