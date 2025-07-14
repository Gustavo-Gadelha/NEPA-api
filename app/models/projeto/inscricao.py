import uuid

from app.extensions import db
from app.models.enums import StatusInscricao
from app.models.mixins import TimestampMixin, LogMixin


class Inscricao(db.Model, TimestampMixin, LogMixin):
    __table_args__ = (db.UniqueConstraint('aluno_id', 'projeto_id', name='uq_inscricao'),)

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = db.Column(db.Enum(StatusInscricao), default=StatusInscricao.PENDENTE, nullable=False)
    bolsista = db.Column(db.Boolean, default=False, nullable=False)

    aluno_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('aluno.id'), nullable=False)
    aluno = db.relationship('Aluno', back_populates='projetos', foreign_keys='Inscricao.aluno_id')

    projeto_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('projeto.id'), nullable=False)
    projeto = db.relationship('Projeto', back_populates='inscricoes', foreign_keys='Inscricao.projeto_id')

    presencas = db.relationship('Presenca', back_populates='inscricao')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
