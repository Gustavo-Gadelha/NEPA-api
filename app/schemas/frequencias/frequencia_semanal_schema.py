from marshmallow_sqlalchemy import fields

from app.extensions import ma
from app.models import FrequenciaSemanal


class FrequenciaSemanalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FrequenciaSemanal
        include_fk = True
        load_instance = True
        dump_only = ('id', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')

    alunos_presentes = fields.Nested('PresencaSchema', many=True, only=('id',))
