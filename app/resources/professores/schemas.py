from app.extensions import ma
from app.models import Professor
from app.models.enums import Autoridade


class ProfessorInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Professor
        load_instance = True

    nome = ma.auto_field(required=True)
    matricula = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    senha = ma.auto_field(required=True)
    telefone = ma.auto_field(required=True)
    curso_id = ma.auto_field(required=True)
    tipo = ma.auto_field(required=True)


class ProfessorPatchInSchema(ma.Schema):
    ativo = ma.Bool()


class ProfessorOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Professor
        include_fk = True

    id = ma.auto_field()
    nome = ma.auto_field()
    matricula = ma.auto_field()
    email = ma.auto_field()
    telefone = ma.auto_field()
    autoridade = ma.Enum(Autoridade, by_value=True, required=True)
    ativo = ma.auto_field()
