from app.extensions import ma
from app.models import Aluno
from app.models.enums import Autoridade


class AlunoInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Aluno
        load_instance = True

    nome = ma.auto_field(required=True)
    matricula = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    senha = ma.auto_field(required=True)
    telefone = ma.auto_field(required=True)
    curso_id = ma.auto_field(required=True)
    tipo = ma.auto_field(required=True)


class AlunoQueryArgsSchema(ma.Schema):
    ativo = ma.Bool()


class AlunoPatchInSchema(ma.Schema):
    ativo = ma.Bool()


class AlunoOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Aluno
        include_fk = True

    id = ma.auto_field()
    nome = ma.auto_field()
    matricula = ma.auto_field()
    email = ma.auto_field()
    telefone = ma.auto_field()
    autoridade = ma.Enum(Autoridade, by_value=True)
    ativo = ma.auto_field()
