from app.models import Professor
from app.schemas.usuarios.usuario_schema import UsuarioSchema


class ProfessorSchema(UsuarioSchema):
    class Meta(UsuarioSchema.Meta):
        model = Professor
