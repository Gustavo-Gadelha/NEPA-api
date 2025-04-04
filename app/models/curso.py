import uuid

from app import db
from app.models.mixins import TimestampMixin, LogMixin


class Curso(db.Model, TimestampMixin, LogMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    sigla = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
