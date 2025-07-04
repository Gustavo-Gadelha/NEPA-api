from flask.views import MethodView
from flask_smorest import Blueprint

from app.jwt import requires_any
from app.models.enums import Autoridade
from .schemas import ProfessorInSchema, ProfessorOutSchema, ProfessorPatchInSchema
from .services import professor_service

professor_blp = Blueprint('professores', __name__, url_prefix='/professores', description='Modulo de professors')


@professor_blp.route('/')
class ProfessorList(MethodView):

    @requires_any(Autoridade.ADMIN)
    @professor_blp.response(200, ProfessorOutSchema(many=True))
    def get(self):
        return professor_service.get_all()

    @requires_any(Autoridade.ADMIN)
    @professor_blp.arguments(ProfessorInSchema)
    @professor_blp.response(201, ProfessorOutSchema)
    def post(self, professor):
        return professor_service.save(professor)


@professor_blp.route('/<uuid:professor_id>')
class ProfessorDetail(MethodView):

    @requires_any(Autoridade.ADMIN)
    @professor_blp.response(200, ProfessorOutSchema)
    def get(self, professor_id):
        return professor_service.get_or_404(professor_id)

    @requires_any(Autoridade.ADMIN)
    @professor_blp.arguments(ProfessorPatchInSchema)
    @professor_blp.response(200, ProfessorOutSchema)
    def patch(self, professor_id, dados):
        return professor_service.update(professor_id, dados)

    @requires_any(Autoridade.ADMIN)
    @professor_blp.response(204)
    def delete(self, professor_id):
        return professor_service.delete_by_id(professor_id)
