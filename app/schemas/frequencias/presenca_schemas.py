from app.extensions import ma
from app.models import Presenca


class PresencaInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Presenca
        load_instance = True

    presente = ma.auto_field(missing=False)
    justificativa = ma.auto_field()
    aluno_id = ma.auto_field(required=True)
    frequencia_semanal_id = ma.auto_field(required=True)


class PresencaOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Presenca
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    presente = ma.auto_field()
    justificativa = ma.auto_field()
    aluno_id = ma.auto_field()
    frequencia_semanal_id = ma.auto_field()
