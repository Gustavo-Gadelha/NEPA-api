from app.core import auto_managed, ModelManager
from app.extensions import db
from app.models.enums import Autoridade
from app.models.usuarios.usuario import Usuario


@auto_managed
class Aluno(Usuario):
    objects = ModelManager()

    id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('usuario.id'), primary_key=True)

    curso_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('curso.id'), nullable=False)
    curso = db.relationship('Curso', foreign_keys='Aluno.curso_id')

    projetos = db.relationship('Inscricao', back_populates='aluno')
    atividades = db.relationship('Atividade', back_populates='aluno')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ativo = True
        self.autoridade = Autoridade.ALUNO

    __mapper_args__ = {
        'polymorphic_identity': 'aluno',
    }
