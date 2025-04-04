from flask_jwt_extended import current_user
from sqlalchemy import func
from sqlalchemy.orm import declarative_mixin, declared_attr

from app import db


@declarative_mixin
class TimestampMixin(object):
    criado_em = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = db.Column(db.DateTime(timezone=True), onupdate=func.now(), nullable=True)


@declarative_mixin
class LogMixin:
    @declared_attr.directive
    def criado_por(cls):
        return db.Column(db.UUID(as_uuid=True), db.ForeignKey('usuario.id'), nullable=True)

    @declared_attr.directive
    def atualizado_por(cls):
        return db.Column(db.UUID(as_uuid=True), db.ForeignKey('usuario.id'), nullable=True)


@db.event.listens_for(LogMixin, 'before_insert')
def before_update_listener(mapper, connection, target):
    if current_user:
        target.criado_por = current_user.id


@db.event.listens_for(LogMixin, 'before_update')
def before_update_listener(mapper, connection, target):
    if current_user:
        target.atualizado_por = current_user.id
