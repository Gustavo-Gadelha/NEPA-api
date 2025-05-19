from uuid import UUID

from werkzeug.exceptions import NotFound

from app import db
from app.models import Inscricao
from app.services.projeto import projeto_service


def save(aluno_id: UUID, projeto_id: UUID) -> Inscricao:
    inscricao = Inscricao(aluno_id=aluno_id, projeto_id=projeto_id)
    projeto = projeto_service.get_or_404(projeto_id)
    projeto.vagas_ocupadas += 1

    db.session.add(inscricao)
    db.session.commit()

    return inscricao


def get_or_404(_id: UUID) -> Inscricao:
    return db.get_or_404(Inscricao, _id)


def get_of_or_404(aluno_id: UUID, projeto_id: UUID) -> Inscricao:
    inscricao: Inscricao | None = db.session.scalar(
        db.select(Inscricao).where(Inscricao.aluno_id == aluno_id, Inscricao.projeto_id == projeto_id)
    )
    if inscricao is None:
        raise NotFound('Relação entre aluno e projeto não encontrado')

    return inscricao


def get_all() -> list[Inscricao]:
    return db.session.scalars(db.select(Inscricao)).all()


def delete(_id: UUID) -> None:
    inscricao: Inscricao = get_or_404(_id)
    db.session.delete(inscricao)
    db.session.commit()


def approve(aluno_id: UUID, projeto_id: UUID) -> Inscricao:
    inscricao = get_of_or_404(aluno_id, projeto_id)
    inscricao.aprovado = True
    db.session.commit()

    return inscricao


def reject(aluno_id: UUID, projeto_id: UUID) -> Inscricao:
    inscricao = get_of_or_404(aluno_id, projeto_id)
    inscricao.aprovado = False
    db.session.commit()

    return inscricao
