from marshmallow.fields import Nested

from app.extensions import ma
from app.models import ControleMensal


class ControleMensalInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ControleMensal
        load_instance = True

    ano = ma.auto_field(required=True)
    mes = ma.auto_field(required=True)
    projeto_id = ma.auto_field(required=True)


class ControleMensalArgsSchema(ma.Schema):
    ano = ma.Int(required=False)
    mes = ma.Int(required=False)
    projeto_id = ma.UUID(required=False)


class ControleMensalOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ControleMensal
        include_fk = True

    id = ma.auto_field()
    ano = ma.auto_field()
    mes = ma.auto_field()
    projeto_id = ma.auto_field()
    frequencias_semanais = Nested('FrequenciaSemanalOutSchema', many=True)
