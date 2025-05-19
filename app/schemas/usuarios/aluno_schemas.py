from app.models import Aluno
from app.schemas.usuarios.usuario_schemas import UsuarioInSchema, UsuarioOutSchema


class AlunoInSchema(UsuarioInSchema):
    class Meta(UsuarioInSchema.Meta):
        model = Aluno


class AlunoOutSchema(UsuarioOutSchema):
    class Meta(UsuarioOutSchema.Meta):
        model = Aluno
