from flask_smorest import Api

from .common import (
    curso_bp
)

from .documentos import (
    edital_bp
)

from .projeto import (
    projeto_bp
)

from .public import (
    auth_bp
)

from .usuarios import (
    aluno_bp,
    professor_bp,
    usuario_bp
)

blueprints = {
    curso_bp: '/cursos',
    edital_bp: '/editais',
    projeto_bp: '/projetos',
    auth_bp: '/auth',
    aluno_bp: '/alunos',
    professor_bp: '/professores',
    usuario_bp: '/usuarios',
}


def register_blueprints(api: Api) -> None:
    for bp, prefix in blueprints.items():
        api.register_blueprint(bp, url_prefix=prefix)
