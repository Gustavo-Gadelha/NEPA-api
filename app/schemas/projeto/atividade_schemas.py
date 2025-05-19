from app.extensions import ma
from app.models import Atividade


class AtividadeInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Atividade
        load_instance = True

    titulo = ma.auto_field(required=True)
    descricao = ma.auto_field()
    exibir = ma.auto_field(missing=True)
    data_inicio = ma.auto_field(required=True)
    data_fim = ma.auto_field(required=True)
    aluno_id = ma.auto_field(required=True)
    projeto_id = ma.auto_field(required=True)


class AtividadeOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Atividade
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    titulo = ma.auto_field()
    descricao = ma.auto_field()
    exibir = ma.auto_field()
    data_inicio = ma.auto_field()
    data_fim = ma.auto_field()
    aluno_id = ma.auto_field()
    projeto_id = ma.auto_field()
