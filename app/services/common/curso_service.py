from uuid import UUID

from app.extensions import db
from app.models import Curso


class CursoService:
    def __init__(self, engine=db):
        self._db = engine

    def save(self, curso: Curso) -> Curso:
        self._db.session.add(curso)
        self._db.session.commit()
        return curso

    def get_or_404(self, _id: UUID) -> Curso:
        return self._db.get_or_404(Curso, _id)

    def get_all(self, *filters) -> list[Curso]:
        if filters:
            stmt = self._db.select(Curso).filter(*filters)
        else:
            stmt = self._db.select(Curso)

        return self._db.session.scalars(stmt).all()

    def delete(self, _id: UUID) -> None:
        curso: Curso = self.get_or_404(_id)
        self._db.session.delete(curso)
        self._db.session.commit()


curso_service = CursoService()
