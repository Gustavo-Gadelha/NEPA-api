from app.extensions import ma
from app.models import ControleMensal, FrequenciaSemanal, Presenca


class ControleMensalInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ControleMensal
        load_instance = True

    ano = ma.auto_field(required=True)
    mes = ma.auto_field(required=True)
    projeto_id = ma.auto_field(required=True)


class ControleMensalOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ControleMensal
        include_fk = True

    id = ma.auto_field()
    ano = ma.auto_field()
    mes = ma.auto_field()
    projeto_id = ma.auto_field()


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
        include_fk = True

    id = ma.auto_field()
    realizada_em = ma.auto_field()
    tempo_inicio = ma.auto_field()
    tempo_termino = ma.auto_field()
    descricao = ma.auto_field()
    observacao = ma.auto_field()


class PresencaInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Presenca
        load_instance = True

    presente = ma.auto_field(required=True)
    justificativa = ma.auto_field()
    aluno_id = ma.auto_field(required=True)
    frequencia_semanal_id = ma.auto_field(required=True)


class PresencaOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Presenca
        include_fk = True

    id = ma.auto_field()
    presente = ma.auto_field()
    justificativa = ma.auto_field()
    aluno_id = ma.auto_field()
