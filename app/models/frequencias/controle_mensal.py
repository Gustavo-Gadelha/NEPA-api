import uuid

from app.core import ModelManager, auto_managed
from app.extensions import db
from app.models.mixins import LogMixin, TimestampMixin


@auto_managed
class ControleMensal(db.Model, TimestampMixin, LogMixin):
    objects = ModelManager()

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ano = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)

    projeto_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('projeto.id'), nullable=False)
    projeto = db.relationship('Projeto', foreign_keys='ControleMensal.projeto_id')

    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('professor.id'), nullable=False)
    professor = db.relationship('Professor', foreign_keys='ControleMensal.professor_id')

    frequencias_semanais = db.relationship('FrequenciaSemanal', back_populates='controle_mensal')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
