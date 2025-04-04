from flask import Flask

from .aluno_routes import aluno_bp
from .auth_routes import auth_bp
from .edital_routes import edital_bp
from .professor_routes import professor_bp
from .projeto_routes import projeto_bp

blueprints = {
    aluno_bp: '/alunos',
    auth_bp: '/auth',
    edital_bp: '/editais',
    professor_bp: '/professores',
    projeto_bp: '/projetos',
}


def register_blueprints(app: Flask) -> None:
    for route, prefix in blueprints.items():
        app.register_blueprint(route, url_prefix=prefix)
