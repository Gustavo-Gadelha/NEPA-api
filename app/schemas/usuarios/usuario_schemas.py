from app.extensions import ma
from app.models import Usuario
from app.models.enums import Autoridade


class UsuarioInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
        load_instance = True

    nome = ma.auto_field(required=True)
    matricula = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    senha = ma.auto_field(required=True)
    telefone = ma.auto_field(required=True)


class UsuarioOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    nome = ma.auto_field()
    matricula = ma.auto_field()
    email = ma.auto_field()
    telefone = ma.auto_field()
    ativo = ma.auto_field()
    autoridade = ma.Enum(Autoridade, by_value=True, required=True)
    tipo = ma.auto_field()
