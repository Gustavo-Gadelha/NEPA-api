from app.extensions import ma
from app.models import FrequenciaSemanal


class FrequenciaSemanalInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = FrequenciaSemanal
        load_instance = True

    realizada_em = ma.auto_field(required=True)
    tempo_inicio = ma.auto_field(required=True)
    tempo_termino = ma.auto_field(required=True)
    descricao = ma.auto_field()
    observacao = ma.auto_field()
    controle_mensal_id = ma.auto_field(required=True)


class FrequenciaSemanalOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = FrequenciaSemanal
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    realizada_em = ma.auto_field()
    tempo_inicio = ma.auto_field()
    tempo_termino = ma.auto_field()
    descricao = ma.auto_field()
    observacao = ma.auto_field()
