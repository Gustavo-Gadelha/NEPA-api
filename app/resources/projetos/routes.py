from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden

from app.jwt import requires_any
from app.models import Projeto
from app.models.enums import Autoridade
from .schemas import (
    ProjetoInSchema,
    ProjetoQueryArgsSchema,
    ProjetoPatchInSchema,
    ProjetoOutSchema
)
from .services import projeto_service

projeto_blp = Blueprint('projetos', __name__, description='Modulo de projetos')


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
        projeto.professor_id = current_user.id
        projeto.curso_id = current_user.curso_id
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
    def patch(self, dados, projeto_id):
        return projeto_service.patch(projeto_id, dados)

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @projeto_blp.response(204)
    def delete(self, projeto_id):
        projeto: Projeto = projeto_service.get_or_404(projeto_id)

        if current_user.autoridade == Autoridade.ADMIN:
            return projeto_service.delete(projeto)
        if not current_user.id == projeto.professor_id:
            raise Forbidden

        return projeto_service.delete(projeto)
