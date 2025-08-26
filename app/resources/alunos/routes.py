from flask_jwt_extended import current_user
from flask_smorest import Blueprint

from app.jwt import requires_any
from app.models import Aluno
from app.models.enums import Autoridade
from app.resources.incricoes import InscricaoOutSchema

from .schemas import AlunoOutSchema, AlunoPatchInSchema, AlunoQueryArgsSchema

aluno_blp = Blueprint('alunos', __name__, url_prefix='/alunos', description='Modulo de alunos')


@aluno_blp.get('/')
@requires_any(Autoridade.ADMIN)
@aluno_blp.arguments(AlunoQueryArgsSchema, location='query', as_kwargs=True)
@aluno_blp.response(200, AlunoOutSchema(many=True))
def get_alunos(**kwargs):
    return Aluno.objects.filter(**kwargs)


@aluno_blp.get('/<uuid:aluno_id>')
@requires_any(Autoridade.ADMIN)
@aluno_blp.response(200, AlunoOutSchema)
def get_aluno(aluno_id):
    return Aluno.objects.get_or_404(aluno_id)


@aluno_blp.patch('/<uuid:aluno_id>')
@requires_any(Autoridade.ADMIN)
@aluno_blp.arguments(AlunoPatchInSchema)
@aluno_blp.response(200, AlunoOutSchema)
def patch_aluno(args, aluno_id):
    return Aluno.objects.patch(aluno_id, args)


@aluno_blp.delete('/<uuid:aluno_id>')
@requires_any(Autoridade.ADMIN)
@aluno_blp.response(204)
def delete_aluno(aluno_id):
    aluno = Aluno.objects.get_or_404(aluno_id)
    return Aluno.objects.delete(aluno)


@aluno_blp.get('/me')
@requires_any(Autoridade.ALUNO)
@aluno_blp.response(200, AlunoOutSchema)
def get_profile_me():
    return Aluno.objects.get_or_404(current_user.id)


@aluno_blp.get('/me/inscricoes')
@requires_any(Autoridade.ALUNO)
@aluno_blp.response(200, InscricaoOutSchema(many=True))
def get_inscricoes_me():
    aluno = Aluno.objects.get_or_404(current_user.id)
    return aluno.inscricoes
