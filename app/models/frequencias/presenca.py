import uuid

from app import db
from app.models.mixins import LogMixin, TimestampMixin


class Presenca(db.Model, TimestampMixin, LogMixin):
    __table_args__ = (db.UniqueConstraint('aluno_id', 'frequencia_semanal_id', name='uq_aluno_frequencia_semanal'),)

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    presente = db.Column(db.Boolean, default=False, nullable=False)
    justificativa = db.Column(db.Text, nullable=True)

    aluno_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('aluno.id'), nullable=False)
    aluno = db.relationship('Aluno', foreign_keys='Presenca.aluno_id', back_populates='presencas')

    frequencia_semanal_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('frequencia_semanal.id'), nullable=False)
    frequencia_semanal = db.relationship('FrequenciaSemanal', back_populates='alunos_presentes')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
