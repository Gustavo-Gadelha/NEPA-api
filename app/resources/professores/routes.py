from flask_jwt_extended import current_user
from flask_smorest import Blueprint

from app.jwt import requires_any
from app.models import Professor
from app.models.enums import Autoridade

from .schemas import ProfessorOutSchema, ProfessorPatchInSchema, ProfessorQueryArgsSchema

professor_blp = Blueprint('professores', __name__, url_prefix='/professores', description='Modulo de professores')


@professor_blp.get('/')
@requires_any(Autoridade.ADMIN)
@professor_blp.arguments(ProfessorQueryArgsSchema, location='query', as_kwargs=True)
@professor_blp.response(200, ProfessorOutSchema(many=True))
def listar_professores(**kwargs):
    return Professor.objects.filter(**kwargs)


@professor_blp.get('/me')
@requires_any(Autoridade.ALUNO)
@professor_blp.response(200, ProfessorOutSchema)
def perfil_me():
    return Professor.objects.get_or_404(current_user.id)


@professor_blp.get('/<uuid:professor_id>')
@requires_any(Autoridade.ADMIN)
@professor_blp.response(200, ProfessorOutSchema)
def get_professor(professor_id):
    return Professor.objects.get_or_404(professor_id)


@professor_blp.patch('/<uuid:professor_id>')
@requires_any(Autoridade.ADMIN)
@professor_blp.arguments(ProfessorPatchInSchema)
@professor_blp.response(200, ProfessorOutSchema)
def patch_professor(dados, professor_id):
    return Professor.objects.patch(professor_id, dados)


@professor_blp.delete('/<uuid:professor_id>')
@requires_any(Autoridade.ADMIN)
@professor_blp.response(204)
def deletar_professor(professor_id):
    professor = Professor.objects.get_or_404(professor_id)
    return Professor.objects.delete(professor)
