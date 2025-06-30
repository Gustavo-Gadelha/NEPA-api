from typing import Type, TypeVar, ClassVar, Optional
from uuid import UUID

from app.extensions import db

M = TypeVar('M', bound='db.Model')


class CRUDService[M]:
    model: ClassVar[Type[M]]

    def __init__(self, engine=db):
        self._db = engine

    def save(self, obj: M) -> M:
        self._db.session.add(obj)
        self._db.session.commit()
        return obj

    def get(self, _id: UUID) -> Optional[M]:
        return self._db.session.get(self.model, _id)

    def get_or_404(self, _id: UUID) -> M:
        return self._db.get_or_404(self.model, _id)

    def get_all(self, *filters) -> list[M]:
        if filters:
            stmt = self._db.select(self.model).filter(*filters)
        else:
            stmt = self._db.select(self.model)

        return self._db.session.scalars(stmt).all()

    def delete(self, _id: UUID) -> None:
        obj = self.get_or_404(_id)
        self._db.session.delete(obj)
        self._db.session.commit()
