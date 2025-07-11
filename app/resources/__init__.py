from flask_smorest import Api

from .alunos import aluno_blp
from .auth import auth_blp
from .cursos import curso_blp
from .editais import edital_blp
from .professores import professor_blp
from .projetos import projeto_blp
from .projetos.incricoes import inscricao_blp

routes = {
    '/auth': auth_blp,
    '/cursos': curso_blp,
    '/editais': edital_blp,
    '/alunos': aluno_blp,
    '/professores': professor_blp,
    '/projetos': {
        '/': projeto_blp,
        '/<uuid:projeto_id>/inscricoes': inscricao_blp
    },
}


def register_blueprints(api: Api, blueprints=None, parent_prefix: str = ''):
    if blueprints is None:
        blueprints = routes

    for prefix, blp in blueprints.items():
        full_prefix = parent_prefix + prefix

        if isinstance(blp, dict):
            register_blueprints(api, blp, full_prefix)
        else:
            api.register_blueprint(blp, url_prefix=full_prefix)
