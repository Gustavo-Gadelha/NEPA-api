import uuid

from sqlalchemy import func

from app import db
from app.models.mixins import TimestampMixin, LogMixin


class ControleMensal(db.Model, TimestampMixin, LogMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ano = db.Column(db.Integer, nullable=False, server_default=func.extract('year', func.now()))
    mes = db.Column(db.Integer, nullable=False, server_default=func.extract('month', func.now()))

    projeto_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('projeto.id'), nullable=False)
    projeto = db.relationship('Projeto')

    frequencias_semanais = db.relationship('FrequenciaSemanal', back_populates='controle_mensal')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
