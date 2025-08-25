import uuid

from app.core import ModelManager, auto_managed
from app.extensions import db
from app.models.mixins import LogMixin, TimestampMixin


@auto_managed
class Curso(db.Model, TimestampMixin, LogMixin):
    objects = ModelManager()

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    sigla = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    professores = db.relationship('Professor', back_populates='curso', foreign_keys='Professor.curso_id')
    alunos = db.relationship('Aluno', back_populates='curso', foreign_keys='Aluno.curso_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
