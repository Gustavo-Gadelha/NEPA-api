from app.extensions import ma
from app.models import ControleMensal


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
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    ano = ma.auto_field()
    mes = ma.auto_field()
    projeto_id = ma.auto_field()
