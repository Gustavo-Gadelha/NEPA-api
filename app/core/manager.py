from typing import Any
from uuid import UUID

from flask import abort


def auto_managed(cls):
    for name, attr in cls.__dict__.items():
        if isinstance(attr, Manager):
            attr.attach_to(cls)
    return cls


class Manager:
    def __init__(self, model_class=None, database=None):
        from app.extensions import db
        self._model_class = model_class
        self._db = database or db

    @property
    def model(self):
        return self._model_class

    def select(self):
        return self._db.select(self.model)

    def query(self):
        return self._db.session.query(self.model)

    def commit(self):
        self._db.commit()

    def attach_to(self, model_class):
        self._model_class = model_class


class ModelManager(Manager):
    def save(self, instance, commit: bool = True):
        self._db.session.add(instance)
        if commit:
            self._db.session.commit()
        return instance

    def create(self, commit: bool = True, **kwargs):
        instance = self.model(**kwargs)
        self._db.session.add(instance)
        if commit:
            self._db.session.commit()
        return instance

    def get(self, ident):
        return self._db.session.get(self.model, ident)

    def get_or_404(self, ident: UUID, description: str | None = None):
        instance = self._db.session.get(self.model, ident)
        if instance is None:
            abort(404, description=description)
        return instance

    def all(self):
        stmt = self._db.select(self.model)
        return self._db.session.scalars(stmt).all()

    def iter_all(self, batch_size: int = 50):
        stmt = self._db.select(self.model).execution_options(yield_per=batch_size)
        return self._db.session.scalars(stmt)

    def paginate(self, page=1, per_page=25, max_per_page=100, count=True, **filters):
        stmt = self._db.session.select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        return self._db.paginate(stmt, page=page, per_page=per_page, max_per_page=max_per_page, count=count)

    def filter(self, **filters):
        stmt = self._db.select(self.model).filter_by(**filters)
        return self._db.session.scalars(stmt).all()

    def exists(self, ident: UUID) -> bool:
        stmt = self._db.select(self._db.exists().where(self.model.id == ident))
        return self._db.session.scalar(stmt)

    def first(self, **filters):
        stmt = self._db.select(self.model).filter_by(**filters).limit(1)
        return self._db.session.scalars(stmt).first()

    def one(self, **filters):
        stmt = self._db.select(self.model).filter_by(**filters)
        return self._db.session.scalar_one(stmt)

    def patch(self, ident: UUID, data: dict[str, Any], allowed_fields: list[str] | None = None, commit: bool = True):
        instance = self.get_or_404(ident)

        if allowed_fields is None:
            allowed_fields = [c.name for c in self.model.__table__.columns if not c.primary_key]

        for key, value in data.items():
            if key in allowed_fields:
                setattr(instance, key, value)
            else:
                abort(400, f"Cannot update field '{key}' in model {self.model.__name__}")

        if commit:
            self._db.session.commit()

        return instance

    def delete(self, instance, commit: bool = True):
        self._db.session.delete(instance)
        if commit:
            self._db.session.commit()
