from flask import Flask
from flask_smorest import Api

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


def register_blueprints(api: Api) -> None:
    for bp, prefix in blueprints.items():
        api.register_blueprint(bp, url_prefix=prefix)
