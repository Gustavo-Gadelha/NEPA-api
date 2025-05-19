from typing import Any
from uuid import UUID

from app import db
from app.config import PASSWORD_LENGTH
from app.models import Aluno
from app.schemas import aluno_schema


def save(dados: dict[str, Any]) -> Aluno:
    aluno: Aluno = aluno_schema.load(dados)
    db.session.add(aluno)
    db.session.commit()
    return aluno


def get_or_404(_id: UUID) -> Aluno:
    return db.get_or_404(Aluno, _id)


def get_all() -> list[Aluno]:
    return db.session.scalars(db.select(Aluno)).all()


def delete(_id: UUID) -> None:
    aluno: Aluno = db.session.scalar(db.select(Aluno).where(Aluno.id == _id))
    db.session.delete(aluno)
    db.session.commit()


def is_valid_password(senha: str) -> bool:
    return senha is not None and len(senha) >= PASSWORD_LENGTH
