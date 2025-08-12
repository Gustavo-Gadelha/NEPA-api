from app.extensions import ma
from app.models import Inscricao
from app.models.enums import StatusInscricao


class InscricaoInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inscricao
        load_instance = True

    aluno_id = ma.auto_field(required=True)
    projeto_id = ma.auto_field(required=True)


class InscricaoQueryArgsSchema(ma.Schema):
    status = ma.Enum(StatusInscricao, required=False, by_value=False)


class InscricaoPatchInSchema(ma.Schema):
    status = ma.Enum(StatusInscricao, required=True, by_value=False)


class InscricaoOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inscricao
        include_fk = True

    id = ma.auto_field()
    status = ma.Enum(StatusInscricao, by_value=True)
    bolsista = ma.auto_field()
    projeto_id = ma.auto_field()

    aluno = ma.Nested('AlunoOutSchema', only=('id', 'nome', 'matricula', 'email', 'telefone'))
