import uuid

from flask_jwt_extended import current_user

from app.core import Manager, ModelManager, auto_managed
from app.extensions import db
from app.models.enums import Autoridade
from app.models.mixins import TimestampMixin


class AccessManager(Manager):
    @staticmethod
    def is_admin():
        return current_user.autoridade == Autoridade.ADMIN

    @staticmethod
    def is_owner(owner_id):
        return current_user.id == owner_id


@auto_managed
class Usuario(db.Model, TimestampMixin):
    objects = ModelManager()
    access = AccessManager()

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    senha = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, default=False, nullable=False)

    autoridade = db.Column(db.Enum(Autoridade), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo,
    }
