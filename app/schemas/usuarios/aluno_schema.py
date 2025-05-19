from app.models import Aluno
from app.schemas.usuarios.usuario_schema import UsuarioSchema


class AlunoSchema(UsuarioSchema):
    class Meta(UsuarioSchema.Meta):
        model = Aluno
