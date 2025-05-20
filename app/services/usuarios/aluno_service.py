from uuid import UUID

from app.extensions import db
from app.models import Aluno


class AlunoService:
    def __init__(self, engine=db):
        self._db = engine

    def save(self, aluno: Aluno) -> Aluno:
        self._db.session.add(aluno)
        self._db.session.commit()
        return aluno

    def get_or_404(self, _id: UUID) -> Aluno:
        return self._db.get_or_404(Aluno, _id)

    def get_all(self, *filters) -> list[Aluno]:
        if filters:
            stmt = self._db.select(Aluno).filter(*filters)
        else:
            stmt = self._db.select(Aluno)

        return self._db.session.scalars(stmt).all()

    def delete(self, _id: UUID) -> None:
        aluno: Aluno = self.get_or_404(_id)
        self._db.session.delete(aluno)
        self._db.session.commit()


aluno_service = AlunoService()
