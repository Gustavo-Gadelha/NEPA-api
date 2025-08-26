from app.core import ModelManager, auto_managed
from app.extensions import db
from app.models.enums import Autoridade
from app.models.usuarios.usuario import Usuario


@auto_managed
class Professor(Usuario):
    objects = ModelManager()

    id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('usuario.id'), primary_key=True)

    curso_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('curso.id'), nullable=False)
    curso = db.relationship('Curso', foreign_keys='Professor.curso_id')

    projetos_propostos = db.relationship('Projeto', back_populates='professor')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ativo = False
        self.autoridade = Autoridade.PROFESSOR

    __mapper_args__ = {
        'polymorphic_identity': 'professor',
    }
