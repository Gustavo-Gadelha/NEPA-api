from typing import Any
from uuid import UUID

from app import db
from app.models import Professor
from app.schemas import professor_schema


def save(dados: dict[str, Any]) -> Professor:
    professor: Professor = professor_schema.load(dados)
    db.session.add(professor)
    db.session.commit()
    return professor


def get_or_404(_id: UUID) -> Professor:
    return db.get_or_404(Professor, _id)


def get_all() -> list[Professor]:
    return db.session.scalars(db.select(Professor)).all()


def delete(_id: UUID) -> None:
    professor: Professor = get_or_404(_id)
    db.session.delete(professor)
    db.session.commit()


def get_all_active() -> list[Professor]:
    return db.session.scalars(db.select(Professor).where(Professor.ativo == True)).all()


def get_all_inactive() -> list[Professor]:
    return db.session.scalars(db.select(Professor).where(Professor.ativo == True)).all()
