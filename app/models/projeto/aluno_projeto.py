import uuid

from app import db


class AlunoProjeto(db.Model):
    __table_args__ = (db.UniqueConstraint('aluno_id', 'projeto_id', name='uq_aluno_projeto'),)

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aprovado = db.Column(db.Boolean, default=False, nullable=False)
    bolsista = db.Column(db.Boolean, default=False, nullable=False)

    aluno_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('aluno.id'), nullable=False)
    aluno = db.relationship('Aluno', back_populates='projetos')

    projeto_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('projeto.id'), nullable=False)
    projeto = db.relationship('Projeto', back_populates='alunos')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
