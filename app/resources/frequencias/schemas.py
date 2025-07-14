from marshmallow_sqlalchemy.fields import Nested

from app.extensions import ma
from app.models import FrequenciaSemanal, Presenca


class FrequenciaSemanalInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = FrequenciaSemanal
        load_instance = True

    realizada_em = ma.auto_field(required=True)
    tempo_inicio = ma.auto_field(required=True)
    tempo_termino = ma.auto_field(required=True)
    descricao = ma.auto_field()
    observacao = ma.auto_field()
    alunos_presentes = Nested('PresencaInSchema', many=True)


class FrequenciaSemanalArgsSchema(ma.Schema):
    realizada_em = ma.Date(required=False)
    controle_mensal_id = ma.UUID(required=False)


class FrequenciaSemanalOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = FrequenciaSemanal
        include_fk = True

    id = ma.auto_field()
    realizada_em = ma.auto_field()
    tempo_inicio = ma.auto_field()
    tempo_termino = ma.auto_field()
    descricao = ma.auto_field()
    observacao = ma.auto_field()
    alunos_presentes = Nested('PresencaOutSchema', many=True)


class PresencaInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Presenca
        load_instance = True

    inscricao_id = ma.auto_field(required=True)
    presente = ma.auto_field(required=True)


class PresencaOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Presenca
        include_fk = True

    inscricao_id = ma.auto_field()
    presente = ma.auto_field()
