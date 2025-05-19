from app.models import Admin
from app.schemas.usuarios.usuario_schemas import UsuarioInSchema, UsuarioOutSchema


class AdminInSchema(UsuarioInSchema):
    class Meta(UsuarioInSchema.Meta):
        model = Admin


class AdminOutSchema(UsuarioOutSchema):
    class Meta(UsuarioOutSchema.Meta):
        model = Admin
