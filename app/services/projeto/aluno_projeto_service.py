from uuid import UUID

from werkzeug.exceptions import NotFound

from app import db
from app.models import AlunoProjeto
from app.services.projeto import projeto_service


def save(aluno_id: UUID, projeto_id: UUID) -> AlunoProjeto:
    aluno_projeto = AlunoProjeto(aluno_id=aluno_id, projeto_id=projeto_id)
    projeto = projeto_service.get_or_404(projeto_id)
    projeto.vagas_ocupadas += 1

    db.session.add(aluno_projeto)
    db.session.commit()

    return aluno_projeto


def get_or_404(_id: UUID) -> AlunoProjeto:
    return db.get_or_404(AlunoProjeto, _id)


def get_of_or_404(aluno_id: UUID, projeto_id: UUID) -> AlunoProjeto:
    aluno_projeto: AlunoProjeto | None = db.session.scalar(
        db.select(AlunoProjeto).where(AlunoProjeto.aluno_id == aluno_id, AlunoProjeto.projeto_id == projeto_id)
    )
    if aluno_projeto is None:
        raise NotFound('Relação entre aluno e projeto não encontrado')

    return aluno_projeto


def get_all() -> list[AlunoProjeto]:
    return db.session.scalars(db.select(AlunoProjeto)).all()


def delete(_id: UUID) -> None:
    aluno_projeto: AlunoProjeto = get_or_404(_id)
    db.session.delete(aluno_projeto)
    db.session.commit()


def approve(aluno_id: UUID, projeto_id: UUID) -> AlunoProjeto:
    aluno_projeto = get_of_or_404(aluno_id, projeto_id)
    aluno_projeto.aprovado = True
    db.session.commit()

    return aluno_projeto


def reject(aluno_id: UUID, projeto_id: UUID) -> AlunoProjeto:
    aluno_projeto = get_of_or_404(aluno_id, projeto_id)
    aluno_projeto.aprovado = False
    db.session.commit()

    return aluno_projeto
