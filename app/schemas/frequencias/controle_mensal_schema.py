from marshmallow_sqlalchemy import fields

from app.extensions import ma
from app.models import ControleMensal


class ControleMensalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ControleMensal
        include_fk = True
        load_instance = True
        dump_only = ('id', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')

    frequencias_semanais = fields.Nested('FrequenciaSemanalSchema', many=True, only=('id',))
