from flask_smorest import Api

from .alunos import aluno_blp
from .auth import auth_blp
from .cursos import curso_blp
from .editais import edital_blp
from .professores import professor_blp
from .projetos import projeto_blp

blueprints = [
    auth_blp,
    curso_blp,
    aluno_blp,
    professor_blp,
    edital_blp,
    projeto_blp,
]


def register_blueprints(api: Api):
    for blp in blueprints:
        api.register_blueprint(blp)
