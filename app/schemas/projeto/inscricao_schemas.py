from app.extensions import ma
from app.models import Inscricao
from app.models.enums import StatusInscricao


class InscricaoInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inscricao
        load_instance = True

    status = ma.Enum(StatusInscricao, by_value=False, missing=StatusInscricao.PENDENTE)
    bolsista = ma.auto_field(missing=False)
    aluno_id = ma.auto_field(required=True)
    projeto_id = ma.auto_field(required=True)


class InscricaoOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inscricao
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    status = ma.Enum(StatusInscricao, by_value=True)
    bolsista = ma.auto_field()
    aluno_id = ma.auto_field()
    projeto_id = ma.auto_field()
