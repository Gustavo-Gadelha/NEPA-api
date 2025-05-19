from typing import Any
from uuid import UUID

from app import db
from app.models import Projeto
from app.models.enums import Situacao
from app.schemas import projeto_schema


def save(dados: dict[str, Any], professor_id: UUID, curso_id: UUID) -> Projeto:
    projeto: Projeto = projeto_schema.load(dados, partial=True)
    projeto.professor_id = professor_id
    projeto.curso_id = curso_id

    db.session.add(projeto)
    db.session.commit()
    return projeto


def get_or_404(_id: UUID) -> Projeto:
    return db.get_or_404(Projeto, _id)


def get_all() -> list[Projeto]:
    return db.session.scalars(db.select(Projeto)).all()


def delete(_id: UUID) -> None:
    projeto: Projeto = get_or_404(_id)
    db.session.delete(projeto)
    db.session.commit()


def get_all_from(professor_id) -> list[Projeto]:
    return db.session.scalars(db.select(Projeto).where(Projeto.professor_id == professor_id)).all()


def get_all_approved() -> list[Projeto]:
    return db.session.scalars(db.select(Projeto).where(Projeto.situacao == Situacao.APROVADO)).all()


def get_all_pending() -> list[Projeto]:
    return db.session.scalars(db.select(Projeto).where(Projeto.situacao == Situacao.PENDENTE)).all()


def change_situation(projeto_id: UUID, situacao: Situacao) -> Projeto:
    projeto: Projeto = get_or_404(projeto_id)
    projeto.situacao = situacao
    db.session.commit()

    return projeto
