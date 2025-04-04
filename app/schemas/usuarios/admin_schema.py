from marshmallow_sqlalchemy import fields

from app.models import Admin
from app.schemas.usuarios.usuario_schema import UsuarioSchema


class AdminSchema(UsuarioSchema):
    class Meta(UsuarioSchema.Meta):
        model = Admin

    editais_criados = fields.Nested('EditalSchema', many=True, only=('id',))
