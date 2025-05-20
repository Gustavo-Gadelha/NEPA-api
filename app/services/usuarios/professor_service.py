from uuid import UUID

from app.extensions import db
from app.models import Professor


class ProfessorService:
    def __init__(self, engine=db):
        self._db = engine

    def save(self, professor: Professor) -> Professor:
        self._db.session.add(professor)
        self._db.session.commit()
        return professor

    def get_or_404(self, _id: UUID) -> Professor:
        return self._db.get_or_404(Professor, _id)

    def get_all(self, *filters) -> list[Professor]:
        if filters:
            stmt = self._db.select(Professor).filter(*filters)
        else:
            stmt = self._db.select(Professor)

        return self._db.session.scalars(stmt).all()

    def delete(self, _id: UUID) -> None:
        professor: Professor = self.get_or_404(_id)
        self._db.session.delete(professor)
        self._db.session.commit()


professor_service = ProfessorService()
