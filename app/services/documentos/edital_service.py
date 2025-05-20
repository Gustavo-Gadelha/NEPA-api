from uuid import UUID

from app.extensions import db
from app.models import Edital


class EditalService:
    def __init__(self, engine=db):
        self._db = engine

    def save(self, edital: Edital) -> Edital:
        self._db.session.add(edital)
        self._db.session.commit()
        return edital

    def get_or_404(self, _id: UUID) -> Edital:
        return self._db.get_or_404(Edital, _id)

    def get_all(self, *filters) -> list[Edital]:
        if filters:
            stmt = self._db.select(Edital).filter(*filters)
        else:
            stmt = self._db.select(Edital)

        return self._db.session.scalars(stmt).all()

    def delete(self, _id: UUID) -> None:
        edital: Edital = self.get_or_404(_id)
        self._db.session.delete(edital)
        self._db.session.commit()


edital_service = EditalService()
