from flask_jwt_extended import current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden

from app.jwt import requires_any
from app.models import Projeto, Usuario
from app.models.enums import Autoridade

from .schemas import ProjetoInSchema, ProjetoOutSchema, ProjetoPatchInSchema, ProjetoQueryArgsSchema

projeto_blp = Blueprint('projetos', __name__, description='Modulo de projetos')


@projeto_blp.get('/')
@projeto_blp.arguments(ProjetoQueryArgsSchema, location='query', as_kwargs=True)
@projeto_blp.response(200, ProjetoOutSchema(many=True))
def get_all_projetos(**kwargs):
    return Projeto.objects.filter(**kwargs)


@projeto_blp.post('/')
@requires_any(Autoridade.PROFESSOR)
@projeto_blp.arguments(ProjetoInSchema)
@projeto_blp.response(201, ProjetoOutSchema)
def post_projeto(projeto):
    projeto.professor_id = current_user.id
    projeto.curso_id = current_user.curso_id
    return Projeto.objects.save(projeto)


@projeto_blp.get('/me')
@requires_any(Autoridade.PROFESSOR)
@projeto_blp.response(200, ProjetoOutSchema(many=True))
def get_all_me_projetos():
    return Projeto.objects.filter(professor_id=current_user.id)


@projeto_blp.get('/<uuid:projeto_id>')
@projeto_blp.response(200, ProjetoOutSchema)
def get_projeto(projeto_id):
    return Projeto.objects.get_or_404(projeto_id)


@projeto_blp.patch('/<uuid:projeto_id>')
@requires_any(Autoridade.ADMIN)
@projeto_blp.arguments(ProjetoPatchInSchema)
@projeto_blp.response(200, ProjetoOutSchema)
def patch_projeto(dados, projeto_id):
    return Projeto.objects.patch(projeto_id, dados)


@projeto_blp.delete('/<uuid:projeto_id>')
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
@projeto_blp.response(204)
def deletar_projeto(projeto_id):
    projeto = Projeto.objects.get_or_404(projeto_id)

    if not Usuario.access.is_admin() and not Usuario.access.is_owner(projeto.professor_id):
        raise Forbidden("Você não tem permissão para deletar este projeto")

    return Projeto.objects.delete(projeto)
