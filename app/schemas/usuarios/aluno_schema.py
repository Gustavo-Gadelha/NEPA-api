from marshmallow_sqlalchemy import fields

from app.extensions import ma
from app.models import Aluno
from app.schemas.usuarios.usuario_schema import UsuarioSchema


class AlunoSchema(UsuarioSchema):
    class Meta(UsuarioSchema.Meta):
        model = Aluno

    curso_id = ma.UUID(required=True)

    projetos = fields.Nested('AlunoProjetoSchema', many=True, only=('id', 'aprovado', 'bolsista'))
