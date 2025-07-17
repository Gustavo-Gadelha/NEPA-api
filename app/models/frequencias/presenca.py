import uuid

from app.extensions import db
from app.models.mixins import LogMixin, TimestampMixin


class Presenca(db.Model, TimestampMixin, LogMixin):
    __table_args__ = (
        db.UniqueConstraint('inscricao_id', 'frequencia_semanal_id', name='uq_inscricao_frequencia_semanal'),
    )

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    presente = db.Column(db.Boolean, default=False, nullable=False)

    inscricao_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('inscricao.id'), nullable=False)
    inscricao = db.relationship('Inscricao', back_populates='presencas')

    frequencia_semanal_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('frequencia_semanal.id'), nullable=False)
    frequencia_semanal = db.relationship('FrequenciaSemanal', back_populates='presencas')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
