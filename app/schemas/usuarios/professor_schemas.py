from app.models import Professor
from app.schemas.usuarios.usuario_schemas import UsuarioInSchema, UsuarioOutSchema


class ProfessorInSchema(UsuarioInSchema):
    class Meta(UsuarioInSchema.Meta):
        model = Professor


class ProfessorOutSchema(UsuarioOutSchema):
    class Meta(UsuarioOutSchema.Meta):
        model = Professor
