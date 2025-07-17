import uuid

from app.extensions import db
from app.models.mixins import TimestampMixin, LogMixin


class FrequenciaSemanal(db.Model, TimestampMixin, LogMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    realizada_em = db.Column(db.Date, nullable=False)
    tempo_inicio = db.Column(db.Time, nullable=False)
    tempo_termino = db.Column(db.Time, nullable=False)

    descricao = db.Column(db.Text, nullable=True)
    observacao = db.Column(db.Text, nullable=True)

    controle_mensal_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('controle_mensal.id'), nullable=False)
    controle_mensal = db.relationship('ControleMensal', back_populates='frequencias_semanais')

    presencas = db.relationship('Presenca', back_populates='frequencia_semanal', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
