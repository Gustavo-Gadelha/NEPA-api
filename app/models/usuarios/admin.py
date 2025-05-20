from app.extensions import db
from app.models.enums import Autoridade
from app.models.usuarios.usuario import Usuario


class Admin(Usuario):
    id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('usuario.id'), primary_key=True)

    editais_criados = db.relationship('Edital', back_populates='admin')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ativo = True
        self.autoridade = Autoridade.ADMIN

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }
