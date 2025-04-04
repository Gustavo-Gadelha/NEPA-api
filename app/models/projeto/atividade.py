import uuid

from app import db
from app.models.mixins import TimestampMixin, LogMixin


class Atividade(db.Model, TimestampMixin, LogMixin):
    __table_args__ = (db.UniqueConstraint('aluno_id', 'projeto_id', name='uq_aluno_projeto_atividade'),)

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    exibir = db.Column(db.Boolean, default=True, nullable=False)

    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)

    aluno_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('aluno.id'), nullable=False)
    aluno = db.relationship('Aluno', back_populates='atividades', foreign_keys='Atividade.aluno_id')

    projeto_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('projeto.id'), nullable=False)
    projeto = db.relationship('Projeto', back_populates='atividades')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
