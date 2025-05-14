from flask_jwt_extended import current_user
from sqlalchemy import func
from sqlalchemy.orm import declarative_mixin, declared_attr

from app import db


@declarative_mixin
class TimestampMixin:
    criado_em = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = db.Column(db.DateTime(timezone=True), server_onupdate=func.now(), nullable=True)


@declarative_mixin
class LogMixin:
    @declared_attr
    def criado_por(cls):
        return db.Column(db.UUID(as_uuid=True), db.ForeignKey('usuario.id'), nullable=True)

    @declared_attr
    def atualizado_por(cls):
        return db.Column(db.UUID(as_uuid=True), db.ForeignKey('usuario.id'), nullable=True)

    @classmethod
    def __declare_last__(cls):
        db.event.listen(cls, 'before_insert', cls._log_criado_por)
        db.event.listen(cls, 'before_update', cls._log_atualizado_por)

    @staticmethod
    def _log_criado_por(mapper, connection, target):
        if current_user and hasattr(target, 'criado_por'):
            target.criado_por = current_user.id

    @staticmethod
    def _log_atualizado_por(mapper, connection, target):
        if current_user and hasattr(target, 'atualizado_por'):
            target.atualizado_por = current_user.id
