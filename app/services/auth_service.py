from typing import Any

from app import db
from app.models.usuarios import Usuario
from app.schemas import aluno_schema, professor_schema


def buscar_usuario(acesso: str) -> Usuario | None:
    if '@' in acesso:
        stmt = db.select(Usuario).where(Usuario.email == acesso)
    else:
        stmt = db.select(Usuario).where(Usuario.matricula == acesso)

    return db.session.scalar(stmt)


def cadastrar_usuario(**kwargs: dict[str, Any]) -> Usuario:
    autoridade = kwargs.get('autoridade', '')
    match autoridade.upper():
        case 'ALUNO':
            return aluno_schema.load(kwargs)
        case 'PROFESSOR':
            return professor_schema.load(kwargs)
        case 'ADMIN':
            raise ValueError('Administradores são cadastrados diretamente no banco')
        case _:
            raise ValueError('Permissão de usuario inválida durante criaçao')
