from flask_smorest import Blueprint

from app.jwt import requires_any
from app.models import Curso
from app.models.enums import Autoridade

from .schemas import CursoInSchema, CursoOutSchema

curso_blp = Blueprint('cursos', __name__, description='Modulo de cursos')


@curso_blp.get('/')
@curso_blp.response(200, CursoOutSchema(many=True))
def get_cursos():
    return Curso.objects.all()


@curso_blp.post('/')
@requires_any(Autoridade.ADMIN)
@curso_blp.arguments(CursoInSchema)
@curso_blp.response(201, CursoOutSchema)
def create_curso(curso):
    return Curso.objects.save(curso)


@curso_blp.get('/<uuid:curso_id>')
@curso_blp.response(200, CursoOutSchema)
def get_curso(curso_id):
    return Curso.objects.get_or_404(curso_id)


@curso_blp.delete('/<uuid:curso_id>')
@requires_any(Autoridade.ADMIN)
@curso_blp.response(204)
def delete_curso(curso_id):
    curso = Curso.objects.get_or_404(curso_id)
    return Curso.objects.delete(curso)
