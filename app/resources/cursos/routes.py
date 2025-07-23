from flask.views import MethodView
from flask_smorest import Blueprint

from app.jwt import requires_any
from app.models.enums import Autoridade

from .schemas import CursoInSchema, CursoOutSchema
from .services import curso_service

curso_blp = Blueprint('cursos', __name__, url_prefix='/cursos', description='Modulo de cursos')


@curso_blp.route('/')
class CursoList(MethodView):

    @curso_blp.response(200, CursoOutSchema(many=True))
    def get(self):
        return curso_service.get_all()

    @requires_any(Autoridade.ADMIN)
    @curso_blp.arguments(CursoInSchema)
    @curso_blp.response(201, CursoOutSchema)
    def post(self, curso):
        return curso_service.save(curso)


@curso_blp.route('/<uuid:curso_id>')
class CursoDetail(MethodView):

    @curso_blp.response(200, CursoOutSchema)
    def get(self, curso_id):
        return curso_service.get_or_404(curso_id)

    @requires_any(Autoridade.ADMIN)
    @curso_blp.response(204)
    def delete(self, curso_id):
        return curso_service.delete_by_id(curso_id)
