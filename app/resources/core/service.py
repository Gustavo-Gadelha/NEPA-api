from typing import ClassVar, Type, Optional, Any
from uuid import UUID

from app.extensions import db


class CRUDService[M]:
    model: ClassVar[Type[M]]

    def __init__(self, engine=db):
        self._db = engine

    def save(self, obj: M) -> M:
        self._db.session.add(obj)
        self._db.session.commit()
        return obj

    def exists(self, _id: UUID) -> bool:
        stmt = self._db.select(self._db.exists().where(self.model.id == _id))
        return self._db.session.scalar(stmt)

    def get(self, _id: UUID) -> Optional[M]:
        return self._db.session.get(self.model, _id)

    def get_or_404(self, _id: UUID) -> M:
        return self._db.get_or_404(self.model, _id)

    def get_all(self, **filters) -> list[M]:
        if filters:
            stmt = self._db.select(self.model).filter_by(**filters)
        else:
            stmt = self._db.select(self.model)

        return self._db.session.scalars(stmt).all()

    def update(self, _id: UUID, dados: dict[Any, str]) -> M:
        obj = self.get_or_404(_id)
        for key, value in dados:
            setattr(obj, key, value)

        self._db.session.commit()
        return obj

    def delete(self, obj: M) -> None:
        self._db.session.delete(obj)
        self._db.session.commit()

    def delete_by_id(self, _id: UUID) -> None:
        obj = self.get_or_404(_id)
        return self.delete(obj)
